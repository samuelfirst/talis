import threading
import json

from talis import config
from talis import log
from talis.kafka.consumer import TalisConsumer


class StdoutConsumer(TalisConsumer, threading.Thread):

    def __init__(self, data_processor, *args, **kwargs):
        TalisConsumer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.set_data_processor(data_processor)
        log.setLevel(config.log_level())

    def run(self):
        for msg in self.consumer:
            #data = self.data_processor.parse(msg.value)
            log.info(msg)
            self.processed += 1
