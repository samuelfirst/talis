import threading
import json

from ..log import log

from ..consumer import TalisConsumer

class StdoutConsumer(TalisConsumer, threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisConsumer.__init__(self, *args, **kwargs)

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            data = json.loads(data)
            log.info(data)
            self.processed += 1