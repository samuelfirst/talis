from kafka import KafkaConsumer

from talis import log
from talis.kafka.base import TalisKafkaBase

class TalisConsumer(TalisKafkaBase):

    def __init__(self, *args, **kwargs):
        self.processed = 0
        self.topic = kwargs['topic']
        del kwargs['topic']
        try:
            self.consumer = KafkaConsumer(self.topic, *args, **kwargs)
            log.info("set consumer to {}".format(self.topic))
        except:
            raise
