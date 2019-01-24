import logging

from unittest import TestCase
from talis import Main


class MainTestCase(TestCase):

    def setUp(self):
        self.config = {
            'host' : 'host_name',
            'port' : 1337,
            'bot_name' : 'imabot',
            'oauth' : 'oauth:132423',
            'log_level' : 10,
            'channel' : 'channel'
        }
        self.main = Main(self.config)
