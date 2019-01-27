import threading

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from .queue import TalisQueue
from .config import *
from .log import log

class TalisKafkaProducer(threading.Thread, TalisQueue):

    def __init__(self, bootstrap_servers=None, kafka_topic=None, queue=None):
        if (bootstrap_servers or queue or kafka_topic) is None:
            raise BaseException("Missing a required attribute in Talis Kafka Producer.")

        threading.Thread.__init__(self)
        TalisQueue.__init__(self, queue)
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.sent = 0
        try:
            self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        except:
            raise

    # ENTRY POINT FOR THREAD
    def run(self):
        while True:
            try:
                data = self.queue.get()
            except:
                break
            try:
                self.producer.send(self.kafka_topic, data)
            except:
                pass
            self.sent += 1
            self.queue.task_done()
        log.info("broken out")
        self.producer.flush()
