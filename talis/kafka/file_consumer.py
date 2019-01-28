import json

from ..consumer import TalisConsumer
from .stop_event import TalisStopEvent

class FileConsumer(TalisConsumer, TalisStopEvent):

    # parse out
    def __init__(self, stop_event):
        TalisStopEvent.__init__(self, stop_event)
        TalisConsumer.__init__(self, *args, **kwargs)

    def run(self):
        with open('./data/debug_'+self.topic'+.txt', 'w') as filehandle:
            for msg in self.consumer:
                data = json.loads(msg.value)
                message = data.get('message')
                filehandle.write(message+"\r\n")
                self.processed += 1
                if self.stop_event.is_set():
                    break
            filehandle.close()
