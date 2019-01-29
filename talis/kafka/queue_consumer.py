import threading
import json

from talis import TalisQueue
from talis import TalisStopEvent
from talis.kafka.consumer import TalisConsumer

class QueueConsumer(threading.Thread, TalisConsumer, TalisQueue, TalisStopEvent):

    def __init__(self, queue, stop_event, data_processor, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisConsumer.__init__(self, data_processor, *args, **kwargs)
        TalisQueue.__init__(self, queue)
        TalisStopEvent.__init__(self, stop_event)

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            self.queue.put_nowait(msg.value)
            self.processed += 1
            if self.stop_event.is_set():
                break
