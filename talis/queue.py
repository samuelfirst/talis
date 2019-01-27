
from queue import Queue

class TalisQueue(object):
    def __init__(self, queue):
        if not isinstance(queue, Queue):
            raise BasicException("Queue needs to bea queue.Queue")
        self.queue = queue
