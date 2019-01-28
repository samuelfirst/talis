import threading

from ..queue import TalisQueue
from ..log import log

from kafka import KafkaProducer

class DequeueProducer(threading.Thread, TalisProducer, TalisQueue):

    def __init__(self, queue, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisProducer.__init__(self, *args, **kwargs)
        TalisQueue.__init__(self, queue)

    # ENTRY POINT FOR THREAD
    def run(self):
        while True:
            try:
                # BLOCKING and THREAD LOCKING
                data = self.queue.get()
            except:
                break
            try:
                self.producer.send(self.topic, data)
            except:
                pass
            self.sent += 1
            self.queue.task_done()
        self.producer.flush() # JON: CHECK THIS FLUSH
