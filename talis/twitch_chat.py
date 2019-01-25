import time
import socket
import re
import fcntl
import os
import errno

class TwitchChat(object):

    def __init__(self, username, oauth, channel="", verbose=False):
        self.username = username
        self.oauth = oauth
        self.verbose = verbose
        self.current_channel = ""
        self.channel = channel
        self.last_sent_time = time.time()
        self.buffer = []
        self.s = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.s.close()

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

        received = s.recv(1024).decode()
        if not TwitchChat._logged_in_successful(received):
            raise IOError("Twitch did not accept the username-oauth "
                          "combination")
        else:
            # ... and they accepted our details
            # Connected to twitch.tv!
            # now make this socket non-blocking on the OS-level
            fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
            if self.s is not None:
                self.s.close()  # close the previous socket
            self.s = s          # store the new socket
            self.join_channel(self.channel)

            # Wait until we have switched channels
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
                    # a "real" error occurred
                    # import traceback
                    # import sys
                    # print(traceback.format_exc())
                    # print("Trying to recover...")
                    self.connect()
                    return result
            else:
                rec = [self._parse_message(line)
                       for line in filter(None, msg.split('\r\n'))]
                rec = [r for r in rec if r]
                result.extend(rec)
