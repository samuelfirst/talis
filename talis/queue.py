import abc

from queue import Queue

class TalisQueue(object):
    def __init__(self, queue):
        if not isinstance(queue, Queue):
            raise TypeError("queue must be a valid `Queue`")
        self.queue = queue
