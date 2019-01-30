
import abc
import threading
import queue

from talis.processor import DataProcessor

class TalisKafkaBase(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @classmethod
    def from_processor(cls, data_processor, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.set_data_processor(data_processor)
        return obj

    @classmethod
    def from_threaded(cls, talis_queue, stop_event, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.set_queue(talis_queue)
        obj.set_stop_event(stop_event)
        return obj

    @classmethod
    def from_threaded_processor(cls, talis_queue, stop_event, data_processor, *args, **kwargs):
        obj = cls(*args, **kwargs)
        obj.set_queue(talis_queue)
        obj.set_stop_event(stop_event)
        obj.set_data_processor(data_processor)
        return obj

    def set_data_processor(self, data_processor):
        if not isinstance(data_processor, DataProcessor):
            raise TypeError("The data_processor must be a valid `talis.DataProcessor` object.")

        self.data_processor = data_processor

    def set_queue(self, talis_queue):
        if not isinstance(talis_queue, queue.Queue):
            raise TypeError("talis_queue must be a valid `queue.Queue` object")

        self.queue = talis_queue

    def set_stop_event(self, stop_event):
        if not isinstance(stop_event, threading.Event):
            raise TypeError("Stop Event must be a valid `threading.Event` object")

        self.stop_event = stop_event
