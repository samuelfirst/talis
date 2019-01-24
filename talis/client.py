import socket

from .connection import Connection
from asyncio import new_event_loop, gather, get_event_loop, sleep

class Client(object):

    def __init__(self, host, port):
        self.connection_config = Connection(host, port)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.eventloop = get_event_loop()

    def run(self):
        self.eventloop.run_until_complete(self.connect())
        try:
            self.eventloop.run_forever()
        finally:
            self.eventloop.stop()

    async def connect(self)
        if self.connected:
            await self.disconnect(expected=True)
        try:
            self.connected = True
            self.connection.connect(self.connection)
        except socket.error as e:
            self.shutdown(msg_error="Failed to connect to socket")

    def shutdown(self, msg_error="Shutting Down.."):
        if self.connected:
            try:
                self.connected = False
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
            except socket.error as e:
                print("{0}: {1}".format(msg_error, e))
                #_l.critical("{0}: {1}".format(msg_error, e))

    def send_command(self, name, value):
        command = "{0} {1}\r\n".format(name, value)
        try:
            print("Sending Command: {0}".format(command))
            #_l.info("Sending Command: {0}".format(command))
            self.connection.send(bytes(command, 'utf-8'))
        except socket.error as e:
            self.shutdown(msg_error="Sending command failed")

    def receive(self):
        return self.connection.recv(1024)
