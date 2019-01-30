import threading

from talis import config
from talis import log
from talis.kafka.producer import TalisProducer

class DequeueProducer(TalisProducer, threading.Thread):

    def __init__(self, queue, *args, **kwargs):
        TalisProducer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.set_queue(queue)
        log.setLevel(config.log_level())

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
        self.producer.flush() # JON: CHECK THIS FLUSH
