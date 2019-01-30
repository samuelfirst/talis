import pytest
import queue
import threading

from talis.kafka import CommandConsumer
from talis.kafka import QueueConsumer
from talis.processor import DataProcessor

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
def mock_data_processor():
    return mock.Mock(spec=DataProcessor, autospec=True)
