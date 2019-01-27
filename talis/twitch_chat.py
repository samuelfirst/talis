import time
import socket
import re
import fcntl
import os
import errno
import threading

from .log import log

class TwitchChat(threading.Thread):

    def __init__(self, username, oauth, channel="", verbose=False,
        queue=None, stop_event=None, central_control=False):
        threading.Thread.__init__(self)
        self.username = username
        self.oauth = oauth
        self.verbose = verbose
        self.current_channel = ""
        self.channel = channel
        self.last_sent_time = time.time()
        self.buffer = []
        self.sent = 0
        self.central_control = central_control
        self.s = None
        if stop_event is None or queue is None:
            raise "Missing variable `stop_event` or `queue`"
        self.stop_event = stop_event
        self.queue = queue

    @staticmethod
    def _logged_in_successful(data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv)'
                    r' NOTICE \* :'
                    r'(Login unsuccessful|Error logging in)*$',
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
        if self.verbose:
            log.info("Send PASS and NICK")

        received = s.recv(1024).decode()
        if not TwitchChat._logged_in_successful(received):
            raise IOError("Twitch did not accept the username-oauth "
                          "combination")
        else:
            if self.verbose:
                log.info("Connected. Taking blocking socket into non-blocking")
            fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
            if self.s is not None:
                self.s.close()
            self.s = s
            self.join_channel(self.channel)

            while self.current_channel != self.channel:
                self.twitch_receive_messages()

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
            log.info(self.buffer)

    def _send_pong(self):
        self._send("PONG")

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

    def run_central_control(self):
        while not self.stop_event.is_set():
            received = self.twitch_receive_messages()

            while not self.queue.empty():
                data = self.queue.get_nowait()
                if data is None:
                    return
                try:
                    self.send_chat_message(data)
                    log.info("Sent chat message {}".format(data))
                except:
                    raise
                self.sent += 1
                self.queue.task_done()
            time.sleep(.01)

    # ENTRY POINT FOR THREADING
    def run(self):
        if self.central_control:
            self.run_central_control()
        while not self.stop_event.is_set():
            received = self.twitch_receive_messages()
            if received:
                username = received[0]["username"]
                msg = received[0]["message"]
                try:
                    if self.verbose:
                        log.info("{0}: {1}".format(username, msg))
                    self.queue.put_nowait(bytes(msg, 'utf-8'))
                except:
                    log.info(e)
                    self.close()
            time.sleep(.01)

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
