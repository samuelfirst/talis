import threading
import json

from talis import log
from talis.kafka.consumer import TalisConsumer

class StdoutConsumer(TalisConsumer, threading.Thread):

    def __init__(self, data_processor, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisConsumer.__init__(self, data_processor, *args, **kwargs)

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            data = json.loads(data)
            log.info(data)
            self.processed += 1
