import threading

from talis import log
from talis.kafka.producer import TalisProducer


class DequeueProducer(TalisProducer, threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        TalisProducer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.set_queue(queue)

    def run(self):
        while True:
            try:
                data = self.queue.get()
            except:
                break
            try:
                self.producer.send(self.topic, data)
            except:
                raise
            self.sent += 1
            self.queue.task_done()
        # JON: CHECK THIS FLUSH
        self.producer.flush()
