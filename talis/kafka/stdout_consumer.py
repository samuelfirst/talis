import threading
from .log import log

from kafka import KafkaConsumer

class StdoutConsumer(TalisConsumer, threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisConsumer.__init__(self, *args, **kwargs)

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            log.info(msg)
            self.processed += 1
