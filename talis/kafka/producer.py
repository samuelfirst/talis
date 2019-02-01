from kafka import KafkaProducer

from talis.kafka.base import TalisKafkaBase


class KafkaProducerFactory(object):

    def __init__(self):
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        if 'topic' in kwargs:
            del kwargs['topic']
        return KafkaProducer(*args, **kwargs)


class TalisProducer(TalisKafkaBase):

    def __init__(self, *args, **kwargs):
        super(TalisProducer, self).__init__()
        self.sent = 0
        self.topic = kwargs['topic']
        self.producer = KafkaProducerFactory.create(*args, **kwargs)
