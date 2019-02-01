import pytest
import threading
import queue

from unittest import mock
from unittest.mock import patch

from talis.kafka import QueueConsumer


class TestQueueConsumer(object):

    def test_init_invalid(
        self, mock_queue, mock_stop_event,
    ):
        with pytest.raises(KeyError):
            queue_consumer = QueueConsumer(
                mock_queue,
                mock_stop_event
            )

    @patch.object(QueueConsumer, 'set_queue')
    @patch.object(QueueConsumer, 'set_stop_event')
    def test_init_valid(
        self, mock_set_stop_event, mock_set_queue,
        mock_queue, mock_stop_event
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            queue_consumer = QueueConsumer(
                mock_queue,
                mock_stop_event,
                topic="topic"
            )

            mock_set_queue.assert_called_with(mock_queue)
            mock_set_stop_event.assert_called_with(mock_stop_event)
