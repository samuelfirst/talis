from unittest import mock
from unittest.mock import patch

import pytest

from talis import TwitchChat


class TestTwitchChat(object):
    @patch.object(TwitchChat, "join_channel")
    @patch("fcntl.fcntl")
    @patch.object(TwitchChat, "_logged_in_successful")
    @patch("socket.socket")
    def test_connect(
        self, mocked_socket, mocked_logged_in, mocked_fcntl, mocked_join_channel
    ):
        mocked_logged_in.return_value = True
        mocked_socket.return_value.recv.return_value.decode.return_value = "data packet"

        twitch_chat = TwitchChat(
            "username",
            "oauth",
            "channel",
            "chat_queue",
            "command_queue",
            "admin_command_queue",
            "stop_event",
        )
        twitch_chat.current_channel = "channel"
        twitch_chat.connect()

        mocked_join_channel.assert_called_with("channel")
        mocked_logged_in.assert_called_with("data packet")
        mocked_socket.return_value.connect.assert_called_with(("irc.twitch.tv", 6667))

        mocked_socket.return_value.connect.side_effect = IOError()
        with pytest.raises(IOError):
            twitch_chat.connect()

        mocked_logged_in.return_value = False
        with pytest.raises(IOError):
            twitch_chat.connect()
