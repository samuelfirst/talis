import threading
import json

from ..queue import TalisQueue
from ..stop_event import TalisStopEvent

from ..consumer import TalisConsumer

class QueueConsumer(threading.Thread, TalisConsumer, TalisQueue, TalisStopEvent):

    def __init__(self, queue, stop_event, data_processor, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisConsumer.__init__(self, data_processor, *args, **kwargs)
        TalisQueue.__init__(self, queue)
        TalisStopEvent.__init__(self, stop_event)

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value)
            self.queue.put_nowait(data)
            self.processed += 1
            if self.stop_event.is_set():
                break
