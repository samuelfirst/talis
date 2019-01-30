import threading
import json

from talis import log
from talis.kafka.consumer import TalisConsumer

class StdoutConsumer(threading.Thread, TalisConsumer):

    def __init__(self, data_processor, *args, **kwargs):
        TalisConsumer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        obj.set_data_processor(data_processor)

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value)
            print(type(msg.value))
            log.info(data)
            self.processed += 1
