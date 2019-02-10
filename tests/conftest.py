import pytest
import queue
import threading

from unittest import mock
from unittest.mock import patch


@pytest.fixture
def mock_kafka_messages():
    return [
        {'channel': "talis_channel", 'message': "test message"},
        {'channel': "talis_channel", 'message': "im a bot"},
        {'channel': "talis_channel", 'message': "no your a bot"},
        {'channel': "talis_channel", 'message': "talis was here"},
        {'channel': "talis_channel", 'message': "python rocks"}
    ]


@pytest.fixture
def mock_commands():
    return {
        '!git': "check out my github",
        '!bot': "yes im a bot",
        "!test": "im testing myself"
    }


@pytest.fixture
def mock_queue():
    return mock.Mock(spec=queue.Queue)


@pytest.fixture
def mock_stop_event():
    return mock.Mock(spec=threading.Event)


@pytest.fixture
def default_env():
    default_env = {
        'HOST_IP': "192.168.1.2",
        'ZOOKEEPER_PORT': 2181,
        'ZOOKEEPER_IP': "zookeeper",
        'KAFKA_PORT': 9092,
        'KAFKA_BOOTSTRAP_HOST': "kafka:9092",
        'TWITCH_CHANNEL': "dotastarladder_en",
        'TWITCH_IRC_HOST_NAME': "irc.chat.twitch.tv",
        'TWITCH_IRC_PORT': 6667,
        'TWITCH_NICK': "talis_jtk",
        'TWITCH_NICK_OAUTH_FILE': ".oauth",
        'BOT_RATE_LIMIT': 20,
        'BOT_RATE_LIMIT_TIME': 30000,
        'LOG_LEVEL': "debug",
        'KAFKA_TOPIC': "twitch_messages",
        'KAFKA_BOT_MESSAGE_TOPIC': "bot_messages"
    }
    return default_env


@pytest.fixture
def unknown_args():
    unknown_args = {
        '-tc': ['--TWITCH_CHANNEL', 'TWITCH_CHANNEL'],
        '-kh': ['--KAFKA_BOOTSTRAP_HOST', 'KAFKA_BOOTSTRAP_HOST'],
        '-n': ['--TWITCH_NICK', 'TWITCH_NICK'],
        '-oa': ['--TWITCH_NICK_OAUTH_FILE', 'TWITCH_NICK_OAUTH_FILE'],
    }
    return unknown_args


@pytest.fixture
def cli_input(request, tmpdir, default_env, unknown_args):
    file_path = tmpdir.mkdir("config").join("test.env")
    with open(file_path, 'w') as fh:
        for i in default_env:
            fh.write("{}: {}\r\n".format(i, default_env[i]))

    import configargparse

    config_parse = configargparse.ArgParser(default_config_files=[file_path])
    for i in unknown_args:
        config_parse.add(
            "{}".format(i),
            unknown_args.get(i)[0],
            env_var=unknown_args.get(i)[1]
        )
    return config_parse
