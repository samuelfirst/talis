import pytest

from talis import TwitchChat

from unittest import mock
from unittest.mock import patch


class TestTwitchChat(object):

    @patch('socket.socket')
    def test_connect(self, mocked_socket):
        pass
