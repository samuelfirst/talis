import pytest
import threading

from unittest import mock
from unittest.mock import patch

from talis.kafka.consumer import KafkaConsumerFactory
from talis.kafka import SpamDetectorConsumer
from talis.processor import DataProcessor


class TestSpamDetectorConsumer(object):

    @patch.object(SpamDetectorConsumer, 'set_data_processor')
    def test_init(
        self, mocked_set_data_processor, mock_queue,
        mock_stop_event, mock_data_processor
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            spam_detector_consumer = SpamDetectorConsumer(
                15, .50, 10,
                mock_queue, mock_stop_event, mock_data_processor,
                topic="topics"
            )
            assert isinstance(spam_detector_consumer, SpamDetectorConsumer)
            mocked_set_data_processor.assert_called_with(mock_data_processor)
            assert spam_detector_consumer.minimum_population == 15
            assert spam_detector_consumer.unique_threshold == .50
            assert spam_detector_consumer.distribution_length_ms == 10

    @pytest.mark.parametrize("valid, expected", [
        (["kappa", "kappa", "kappa"], 1.00),
        (["kappa", "test", "kappa"], .67),
        (["test", "test15", "test16"], .33),
        (["test", "test15", "test16", "kappa", "kapp"], .20)
    ])
    def test_calculate_unique_distribution(
        self, mock_queue, mock_stop_event,
        mock_data_processor, valid, expected
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            spam_detector_consumer = SpamDetectorConsumer(
                15, .50, 10,
                mock_queue, mock_stop_event, mock_data_processor,
                topic="topics"
            )
            spam_detector_consumer.message_bin = valid
            r = spam_detector_consumer.calculate_unique_distribution()
            assert "{:.2f}".format(r) == "{:.2f}".format(expected)

    @pytest.mark.parametrize("data, expected", [
        ("kkkkkkkkk", "kkkkkkkkk"),
        ("testing a collapse", "testing a collapse"),
        ("Kappa Kappa Kappa", "kappa"),
        ("Kappa kappa kappa", "kappa")
    ])
    def test_collapse_message(
        self, mock_queue, mock_stop_event,
        mock_data_processor, data, expected
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            spam_detector_consumer = SpamDetectorConsumer(
                15, .50, 10,
                mock_queue, mock_stop_event, mock_data_processor,
                topic="topics"
            )
            assert spam_detector_consumer.collapse_message(data) == expected

    def test_send_bot_message(
        self, mock_queue, mock_stop_event,
        mock_data_processor, data, expected
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_producer:
            spam_detector_consumer = SpamDetectorConsumer(
                15, .50, 10,
                mock_queue, mock_stop_event, mock_data_processor,
                topic="topics"
            )
            spam_detector_consumer.message_bin = [
                "Kappa", "test", "talis"
            ]
            spam_detector_consumer.send_bot_message()

    def test_process_message(self):
        pass
