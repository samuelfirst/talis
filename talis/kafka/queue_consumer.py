import threading
import json

from talis.kafka.consumer import TalisConsumer


class QueueConsumer(TalisConsumer, threading.Thread):

    def __init__(self, queue, stop_event, *args, **kwargs):
        TalisConsumer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.set_queue(queue)
        self.set_stop_event(stop_event)

    def run(self):
        for msg in self.consumer:
            self.queue.put_nowait(msg.value)
            self.processed += 1
            if self.stop_event.is_set():
                break
