
from .queue_consumer import QueueConsumer

class CommandConsumer(QueueConsumer):

    def __init__(self, commands, queue, stop_event, *args, **kwargs):
        super().__init__(queue, stop_event, *args, **kwargs)
        self.commands = commands

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                msg_d = msg.value.decode('utf-8')
                if msg_d in self.commands.keys():
                    response = self.commands[msg_d]
                    self.queue.put_nowait(response)
                    self.processed += 1
            if self.stop_event.is_set():
                break
