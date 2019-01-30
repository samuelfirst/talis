import threading

from talis.kafka.consumer import TalisConsumer

class DequeueProducer(TalisConsumer):

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
