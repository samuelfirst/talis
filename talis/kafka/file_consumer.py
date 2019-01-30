import json

from talis.kafka.consumer import TalisConsumer

class FileConsumer(TalisConsumer):

    def __init__(self, data_processor, *args, **kwargs):
        super(FileConsumer, self).__init__(self, *args, **kwargs)
        self.set_data_processor(data_processor)

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
