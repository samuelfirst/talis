import pytest
import threading

from unittest import mock
from unittest.mock import patch

from talis.kafka import FileConsumer
from talis.processor import DataProcessor


class TestFileConsumer(object):

    def test_init_invalid(
        self, mock_stop_event, mock_data_processor
    ):
        with pytest.raises(KeyError):
            file_consumer = FileConsumer(
                mock_stop_event,
                mock_data_processor
            )

    @patch.object(FileConsumer, 'set_stop_event')
    @patch.object(FileConsumer, 'set_data_processor')
    def test_init_valid(
        self, mock_set_data_proessor, mock_set_stop_event,
        mock_stop_event, mock_data_processor
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            file_consumer = FileConsumer(
                mock_stop_event,
                mock_data_processor,
                topic="topic"
            )

            mock_set_stop_event.assert_called_with(mock_stop_event)
            mock_set_data_proessor.assert_called_with(mock_data_processor)

    def test_formatted_file_name(
        self, mock_stop_event, mock_data_processor, monkeypatch
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:

            file_consumer = FileConsumer(
                mock_stop_event,
                mock_data_processor,
                topic="topic"
            )
            file_consumer.full_path = '/data_{}.txt'

            assert file_consumer.formatted_file_name() == "/data_topic.txt"

    def test_process_message(
        self, mock_stop_event, mock_data_processor
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:

            file_consumer = FileConsumer(
                mock_stop_event,
                mock_data_processor,
                topic="topic"
            )
