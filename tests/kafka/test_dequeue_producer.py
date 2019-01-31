import pytest
import queue
import threading

from unittest import mock
from unittest.mock import patch

from talis.kafka import DequeueProducer

from kafka import KafkaProducer


class TestDequeueProducer(object):

    def test_init_invalid(
        self, mock_queue
    ):
        with pytest.raises(KeyError):
            command_consumer = DequeueProducer(
                mock_queue
            )

    @patch.object(DequeueProducer, 'set_queue')
    def test_init_valid(
        self, mock_set_queue, mock_queue
    ):
        with mock.patch(
            'talis.kafka.producer.KafkaProducerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            command_consumer = DequeueProducer(
                mock_queue,
                topic="test"
            )
            mock_set_queue.assert_called_with(mock_queue)
