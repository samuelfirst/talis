'''
Use this script to debug a kafka topic.
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import argparse
import threading

from talis.config import *
from talis.log import log
from talis.consumer import TalisKafkaConsumer
from talis.stop_event import TalisStopEvent

class KafkaTopicToFile(TalisKafkaConsumer, TalisStopEvent):

    # parse out
    def __init__(self, kafka_topic, stop_event, bootstrap_servers="", auto_offset_reset=""):
        TalisKafkaConsumer.__init__(self, kafka_topic, bootstrap_servers=bootstrap_servers, auto_offset_reset=auto_offset_reset)
        TalisStopEvent.__init__(self, stop_event)

    def run(self):
        with open('./data/twitch_messages.txt', 'w') as filehandle:
            for msg in self.consumer:
                filehandle.write(msg.value.decode('utf-8')+"\r\n")
                log.info("{}".format(self.processed))
                self.processed += 1
                if self.stop_event.is_set():
                    break
            filehandle.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Debug a kafka topic')
    parser.add_argument(
        'host', metavar='host', type=str, nargs='?',
        default=os.getenv("KAFKA_BOOTSTRAP_HOST"),
        help='The kafka host (bootstrap)'
    )
    parser.add_argument(
        'offset', metavar='offset', type=str, nargs='?',
        default='latest',
        help='The offset of the kafka offset to start from (latest|earliest)'
    )
    parser.add_argument(
        'kafka_topic', metavar='kafka_topic', type=str, nargs='?',
        default=os.getenv("KAFKA_TOPIC"),
        help='The kafka topic you want to debug'
    )

    args = parser.parse_args()
    host = args.host
    offset = args.offset
    kafka_topic = args.kafka_topic

    log.info("Arguments: {}".format(args))

    consumer_stop_event = threading.Event()

    try:
        consumer = KafkaTopicToFile(
            kafka_topic,
            consumer_stop_event,
            bootstrap_servers=host,
            auto_offset_reset=offset
        )
        consumer.start()
    except:
        consumer_stop_event.set()
        raise
