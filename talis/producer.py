
from kafka import KafkaProducer

class TalisProducer(object):

    def __init__(self, *args, **kwargs):
        self.sent = 0
        self.topic = kwargs['topic']
        del kwargs['topic']
        try:
            self.producer = KafkaProducer(*args, **kwargs)
        except:
            raise
