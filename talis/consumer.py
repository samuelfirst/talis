import threading

from kafka import KafkaConsumer

class TalisKafkaConsumer(threading.Thread):

    def __init__(self, bootstrap_servers=None, kafka_topic=None, stop_event=None, offset=None):
        '''
            TODO: Could use other args for kafka consumer
        '''
        if (bootstrap_servers or kafka_topic or stop_event) is None:
            raise BaseException("Missing a required attribute in Talis Kafka Consumer.")

        threading.Thread.__init__(self)
        self.processed = 0
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.stop_event = stop_event
        try:
            self.consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers=self.bootstrap_servers, auto_offset_reset=offset)
        except:
            pass
