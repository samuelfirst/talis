import threading

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from .config import *
from .log import log

class TalisKafkaProducer(threading.Thread):

    def __init__(self, bootstrap_servers=None, kafka_topic=None, queue=None):
        if (bootstrap_servers or queue or kafka_topic or stop_event) is None:
            raise BaseException("Missing a required attribute in Talis Kafka Producer.")

        threading.Thread.__init__(self)
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.queue = queue
        self.sent = 0
        try:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        except:
            pass

    def run(self):
        while True:
            data = self.queue.get()

            if data is None:
                self.queue.task_done()
                return
            try:
                self.producer.send(self.kafka_topic, data)
            except:
                pass
            self.sent += 1
            self.queue.task_done()
        self.producer.flush()
