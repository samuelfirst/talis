from kafka import KafkaConsumer

from talis import log
from talis.kafka.base import TalisKafkaBase


class KafkaConsumerFactory(object):

    def __init__(self):
        pass

    @classmethod
    def create(cls, kafka_topic, *args, **kwargs):
        if 'topic' in kwargs:
            del kwargs['topic']
        return KafkaConsumer(kafka_topic, *args, **kwargs)


class TalisConsumer(TalisKafkaBase):

    def __init__(self, *args, **kwargs):
        super(TalisConsumer, self).__init__()
        self.processed = 0
        self.topic = kwargs['topic']
        self.consumer = KafkaConsumerFactory.create(
            self.topic, *args, **kwargs
        )
