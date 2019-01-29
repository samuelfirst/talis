import threading

from talis import TalisQueue
from talis.kafka.producer import TalisProducer

class DequeueProducer(threading.Thread, TalisProducer, TalisQueue):

    def __init__(self, queue, data_processor, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisProducer.__init__(self, data_processor, *args, **kwargs)
        TalisQueue.__init__(self, queue)

    def run(self):
        while True:
            try:
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
