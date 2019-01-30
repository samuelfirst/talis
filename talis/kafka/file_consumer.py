import threading

from talis.kafka.consumer import TalisConsumer

class FileConsumer(TalisConsumer, threading.Thread):

    def __init__(self, stop_event, data_processor, *args, **kwargs):
        TalisConsumer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.set_stop_event(stop_event)
        self.set_data_processor(data_processor)

    def run(self):
        with open("./data/debug_{}.txt".format(self.topic), 'w') as filehandle:
            for msg in self.consumer:
                data = self.data_processor.parse(msg.value)
                message = data.get('message')
                filehandle.write(message+"\r\n")
                self.processed += 1
                if self.stop_event.is_set():
                    filehandle.close()
                    break
            filehandle.close()
