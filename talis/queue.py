
from queue import Queue

class InvalidQueueException(Exception):
    '''Raised when a queue is not a valid queue object'''
    pass

class TalisQueue(object):
    def __init__(self, queue):
        if not isinstance(queue, Queue):
            raise InvalidQueueException("The queue argument must be a valie queue.Queue object.")

        self.queue = queue
