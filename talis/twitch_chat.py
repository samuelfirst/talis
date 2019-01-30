import time
import socket
import re
import fcntl
import os
import errno
import threading

from talis import log
from talis.processor import JsonProcessor

class TwitchChat(threading.Thread):

    def __init__(self, username, oauth,
                channel, chat_queue, command_queue,
                stop_event):
        threading.Thread.__init__(self)
        self.username = username
        self.oauth = oauth
        self.current_channel = ""
        self.channel = channel
        self.last_sent_time = time.time()
        self.buffer = []
        self.sent = 0
        self.s = None
        self.stop_event = stop_event
        self.chat_queue = chat_queue
        self.command_queue = command_queue
        self.data_processor = JsonProcessor()

    @staticmethod
    def _logged_in_successful(data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv)'
                    r' NOTICE \* :'
                    r'(Login unsuccessful|Error logging in|Improperly formatted auth)*$',
                    data.strip()):
            return False
        else:
            return True

    @staticmethod
    def _check_has_ping(data):
        return re.match(
            r'^PING :tmi\.twitch\.tv$', data)

    @staticmethod
    def _check_has_channel(data):
        return re.findall(
            r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+'
            r'\.tmi\.twitch\.tv '
            r'JOIN #([a-zA-Z0-9_]+)$', data)

    @staticmethod
    def _check_has_message(data):
        return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+'
                        r'\.tmi\.twitch\.tv '
                        r'PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_host = "irc.twitch.tv"
        connect_port = 6667
        try:
            s.connect((connect_host, connect_port))
        except (Exception, IOError):
            print("Unable to create a socket to %s:%s" % (
                connect_host,
                connect_port))
            raise  # unexpected, because it is a blocking socket

        s.send(('PASS %s\r\n' % self.oauth).encode('utf-8'))
        s.send(('NICK %s\r\n' % self.username).encode('utf-8'))
        log.debug("Sent PASS and NICK")

        received = s.recv(1024).decode()
        if not TwitchChat._logged_in_successful(received):
            raise IOError("Twitch did not accept the username-oauth "
                          "combination")
        else:
            log.debug("Connected. Taking blocking socket into non-blocking")
            fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
            if self.s is not None:
                log.info("Closed socket :(")
                self.s.close()
            self.s = s
            self.join_channel(self.channel)

            while self.current_channel != self.channel:
                self.twitch_receive_messages()
            else:
                log.info("JOINED {0}".format(self.channel))

    def _push_from_buffer(self):
        if len(self.buffer) > 0:
            if time.time() - self.last_sent_time > 5:
                try:
                    message = self.buffer.pop(0)
                    self.s.send(message.encode('utf-8'))
                finally:
                    self.last_sent_time = time.time()

    def _send(self, message):
        if len(message) > 0:
            self.buffer.append(message + "\n")

    def _send_pong(self):
        self._send("PONG")
        log.debug("SENT PONG")

    def join_channel(self, channel):
        self.s.send(('JOIN #%s\r\n' % channel).encode('utf-8'))

    def send_chat_message(self, message):
        self._send("PRIVMSG #{0} :{1}".format(self.channel, message))

    def _parse_message(self, data):
        if TwitchChat._check_has_ping(data):
            self._send_pong()
        if TwitchChat._check_has_channel(data):
            self.current_channel = TwitchChat._check_has_channel(data)[0]

        if TwitchChat._check_has_message(data):
            return {
                'channel': re.findall(r'^:.+![a-zA-Z0-9_]+'
                                      r'@[a-zA-Z0-9_]+'
                                      r'.+ '
                                      r'PRIVMSG (.*?) :',
                                      data)[0],
                'username': re.findall(r'^:([a-zA-Z0-9_]+)!', data)[0],
                'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0]
            }
        else:
            return None

    def close(self):
        self.s.close()

    def run(self):
        while not self.stop_event.is_set():
            received = self.twitch_receive_messages()
            if received:
                username = received[0]["username"]
                msg = received[0]["message"]
                try:
                    log.debug("{0}: {1}".format(username, msg))
                    data = {'channel' : self.channel, 'username': username, 'message': msg}
                    self.chat_queue.put_nowait(bytes(self.data_processor.format(data), 'utf-8'))
                    log.info("send to chat_queue {}".format(msg))
                except:
                    self.close()

            while not self.command_queue.empty():
                data = self.command_queue.get_nowait()
                if data is None:
                    return
                try:
                    data = self.data_processor.parse(data)
                    message = data.get('message')
                    self.send_chat_message(message)
                    log.debug("Sent chat message {}".format(message))
                except:
                    raise
                self.sent += 1
                self.command_queue.task_done()
            time.sleep(0.01)

    def twitch_receive_messages(self):
        self._push_from_buffer()
        result = []
        while True:
            try:
                msg = self.s.recv(4096).decode()
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    return result
                else:
                    self.connect()
                    return result
            else:
                rec = [self._parse_message(line)
                       for line in filter(None, msg.split('\r\n'))]
                rec = [r for r in rec if r]
                result.extend(rec)
