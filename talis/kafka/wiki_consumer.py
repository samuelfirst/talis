import threading
import re

from talis import log

from talis.kafka.queue_consumer import QueueConsumer

from talis.vendor import Wikipedia
from talis.algos import TFIDF


class WikiConsumer(QueueConsumer, threading.Thread):
    '''
        TODO: Clean up this class. It was for getting
        out a quick demo of wikipedia interaction.
    '''
    def __init__(self, queue, stop_event,
                 data_processor, *args, **kwargs):
        QueueConsumer.__init__(self, queue, stop_event, *args, **kwargs)
        threading.Thread.__init__(self)
        self.set_data_processor(data_processor)
        self.wiki = Wikipedia()
        self.algo = TFIDF()

    def process_message(self, msg):
        data = self.data_processor.parse(msg)

        command = data.get('message')

        test = re.findall(r'(^!wiki )(\".+\") (.+)', command)

        if test and len(test[0]) == 3:
            test = test[0]
            command = test[0].strip()
            topic = test[1].replace('"', "")
            question = test[2]
            print(command, topic, question)
        else:
            command = False

        if command == '!wiki':
            print("setting wiki")
            try:
                self.algo.set_data(self.wiki.get_content(topic))
            except:
                raise

            response = self.algo.answer(question)
            if response is not None:

                data_to_send = {
                    'channel': data.get('channel'),
                    'message': response
                }
                self.queue.put_nowait(
                    bytes(
                        self.data_processor.format(data_to_send),
                        'utf-8'
                    )
                )
                log.info('RULES BASED COMMAND {}'.format(command))
                self.processed += 1

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                self.process_message(msg.value)
            if self.stop_event.is_set():
                break
