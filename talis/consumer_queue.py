''''
Use this class to pipe a kafka topic into a queue for further processing
'''
import threading

from kafka import KafkaConsumer
from .queue import TalisQueue
from .stop_event import TalisStopEvent

class TalisKafkaConsumerQueue(threading.Thread, TalisQueue, TalisStopEvent):

    def __init__(self, kafka_topic, stop_event, bootstrap_servers=None, auto_offset_reset=None, queue=""):
        '''
            TODO: Could use other args for kafka consumer
        '''
        if (bootstrap_servers or kafka_topic or stop_event) is None:
            raise BaseException("Missing a required attribute in Talis Kafka Consumer.")

        threading.Thread.__init__(self)
        TalisQueue.__init__(self, queue)
        TalisStopEvent.__init__(self, stop_event)
        self.processed = 0
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.auto_offset_reset =auto_offset_reset
        try:
            self.consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers=self.bootstrap_servers, auto_offset_reset=self.auto_offset_reset)#, consumer_timeout_ms=400)
        except:
            raise

    # ENTRY POINT FOR THREAD
    def run(self):
        for msg in self.consumer:
            self.queue.put_nowait(msg.value.decode('utf-8'))
            print("Sent a queue message {}".format(msg.value.decode('utf-8')))
            self.processed += 1
            if self.stop_event.is_set():
                break
