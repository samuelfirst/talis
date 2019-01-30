import pytest
import queue
import threading

from unittest import mock
from unittest.mock import patch

from talis.kafka import CommandConsumer


class TestCommandConsumer(object):

    @patch.object(CommandConsumer, 'set_data_processor')
    def test_init_invalid(
        self, mock_set_data_processor, mock_queue,
        mock_stop_event, mock_data_processor,
        mock_commands
    ):
        with pytest.raises(KeyError):
            command_consumer = CommandConsumer(
                mock_commands,
                mock_queue,
                mock_stop_event,
                mock_data_processor
            )

    @patch.object(CommandConsumer, 'set_data_processor')
    def test_init_valid(
        self, mock_set_data_processor, mock_queue,
        mock_stop_event, mock_data_processor,
        mock_commands
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_consumer:
            command_consumer = CommandConsumer(
                mock_commands,
                mock_queue,
                mock_stop_event,
                mock_data_processor,
                topic="test"
            )

            mock_set_data_processor.assert_called_with(mock_data_processor)
            assert command_consumer.commands == mock_commands

    def test_process_message(
        self, mock_commands, mock_kafka_messages,
        mock_queue, mock_stop_event, mock_data_processor
    ):
        with mock.patch(
            'talis.kafka.consumer.KafkaConsumerFactory.create',
            return_value=None
        ) as mocked_kafka_consumer:
            command_consumer = CommandConsumer(
                mock_commands, mock_queue,
                mock_stop_event, mock_data_processor,
                topic="twitch_message"
            )

            processed = 0
            for data in mock_kafka_messages:
                command_consumer.process_message(data)
                command_consumer.data_processor.parse.assert_called_with(data)
                if data.get('message') in mock_commands.keys():
                    command_consumer.queue.put_nowait.assert_called()
                    assert command_consumer.processed == processed + 1
                processed += 1
