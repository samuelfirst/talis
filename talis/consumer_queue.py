from .consumer import TalisKafkaConsumer

class TalisConsumerQueue(TalisKafkaConsumer):

    def __init__(self, queue, *args, **kwargs):
        super().__init__(queue, *args, **kwargs)
        self.queue = queue

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            self.queue.put_nowait(msg.value)
            self.processed += 1
            if self.stop_event.is_set():
                break
