import threading

from talis.kafka.consumer import TalisConsumer


class FileConsumer(TalisConsumer, threading.Thread):

    def __init__(self, stop_event, data_processor, *args, **kwargs):
        TalisConsumer.__init__(self, *args, **kwargs)
        threading.Thread.__init__(self)

        self.full_path = "./data/debug_{}.txt"
        self._open_file = None

        self.set_stop_event(stop_event)
        self.set_data_processor(data_processor)

    def formatted_file_name(self):
        return str(self.full_path).format(self.topic)

    def process_message(self, msg):
        if self._open_file is None:
            self._set_open_file()

        data = self.data_processor.parse(msg)
        message = data.get('message')
        self._open_file.write(f"{message}\r\n")
        self.processed += 1

    def _set_open_file(self):
        self._open_file = open(self.formatted_file_name(), 'w')

    def _close_open_file(self):
        if self._open_file is not None:
            self._open_file.close()

    def run(self):
        for msg in self.consumer:
            self.process_message(msg.value)
            if self.stop_event.is_set() or msg.value is None:
                self._close_open_file()
                break
