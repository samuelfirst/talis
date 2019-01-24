from unittest import TestCase

from . import *
from talis.connection import Connection

class ConnectionTest(TestCase):

    def setUp(self):
        self.host = 'host'
        self.port = 1337
        self.connection = Connection(self.host, self.port)

    def tearDown(self):
        del self.connection

    def test_connection_host(self):
        assert self.connection.host == self.host

    def test_connection_port(self):
        assert self.connection.port == self.port
