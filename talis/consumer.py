
from kafka import KafkaConsumer

class TalisConsumer(object):

    def __init__(self, *args, **kwargs):
        self.processed = 0
        self.topic = kwargs['topic']
        del kwargs['topic']
        try:
            self.consumer = KafkaConsumer(self.topic, *args, **kwargs)
        except:
            raise
