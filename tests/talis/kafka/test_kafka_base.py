import pytest
import queue
import threading

from talis.processor import DataProcessor
from talis.kafka.base import TalisKafkaBase


class TestTalisKafkaBase(object):

    def test_init_from_processor(self, mock_data_processor):
        talis_base = TalisKafkaBase.from_processor(mock_data_processor)
        assert isinstance(talis_base, TalisKafkaBase)
        assert isinstance(talis_base.data_processor, DataProcessor)

    def test_init_from_threaded(self, mock_queue, mock_stop_event):
        talis_base = TalisKafkaBase.from_threaded(
            mock_queue,
            mock_stop_event
        )
        assert isinstance(talis_base, TalisKafkaBase)
        assert isinstance(talis_base.queue, queue.Queue)
        assert isinstance(talis_base.stop_event, threading.Event)

    def test_init_from_threaded_processor(
        self,
        mock_queue,
        mock_stop_event,
        mock_data_processor
    ):
        talis_base = TalisKafkaBase.from_threaded_processor(
            mock_queue,
            mock_stop_event,
            mock_data_processor
        )
        assert isinstance(talis_base, TalisKafkaBase)
        assert isinstance(talis_base.queue, queue.Queue)
        assert isinstance(talis_base.stop_event, threading.Event)
        assert isinstance(talis_base.data_processor, DataProcessor)
