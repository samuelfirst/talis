from kafka import KafkaProducer

from talis.kafka.base import TalisKafkaBase

class TalisProducer(TalisKafkaBase):

    def __init__(self, *args, **kwargs):
        super(TalisProducer, self).__init__()
        self.sent = 0
        self.topic = kwargs['topic']
        del kwargs['topic']
        try:
            self.producer = KafkaProducer(*args, **kwargs)
        except:
            raise
