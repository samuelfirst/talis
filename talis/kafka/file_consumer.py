import json

from talis import TalisConsumer
from talis import TalisStopEvent

class FileConsumer(TalisConsumer, TalisStopEvent):

    # parse out
    def __init__(self, stop_event, data_processor, *args, **kwargs):
        TalisStopEvent.__init__(self, stop_event)
        TalisConsumer.__init__(self, data_processor, *args, **kwargs)

    def run(self):
        with open("./data/debug_{}.txt".format(self.topic), 'w') as filehandle:
            for msg in self.consumer:
                data = json.loads(msg.value)
                message = data.get('message')
                filehandle.write(message+"\r\n")
                self.processed += 1
                if self.stop_event.is_set():
                    break
            filehandle.close()
