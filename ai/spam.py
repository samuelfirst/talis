'''
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated

Actually a Host Giveway "Feature"

'''
'''
Use this script to debug a kafka topic.
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
import argparse
import threading
import collections
from queue import Queue

from talis.config import *
from talis.log import log
from talis.consumer_queue import TalisKafkaConsumerQueue
from talis.producer import TalisKafkaProducer

def log_info(msg):
    print("AI SPAM: {}".format(msg))

class SpamDetectorConsumer(TalisKafkaConsumerQueue):

    def __init__(self, minimum_population,
            unique_threshold, distribution_length_ms,
            kafka_topic, stop_event,
            bootstrap_servers="",
            auto_offset_reset="",
            queue=""):
        super().__init__(kafka_topic, stop_event, bootstrap_servers=bootstrap_servers, auto_offset_reset=auto_offset_reset, queue=queue)
        self.message_bin = []
        self.minimum_population = minimum_population
        self.unique_threshold = unique_threshold
        self.force_reset = False
        self.start_time = time.time()
        self.distribution_length_ms = distribution_length_ms

    def calculate_unique_distribution(self):
        bin_len = len(self.message_bin)
        counter = collections.Counter(map(lambda x : x.lower(), self.message_bin))
        most_common_count = counter.most_common(1)[0][1]
        r = most_common_count/bin_len
        log_info("{0:.2f}% of {1:.2f}% threshold".format(r*100, unique_threshold*100))
        return r

    def collapse_message(self, msg):
        m_split = msg.decode('utf-8').lower().split(" ")
        bin_len = len(m_split)
        unique = len(list(set(map(lambda x : x.lower(),m_split))))
        if bin_len > 1 and unique == 1:
            log_info("DUPLICATE SPAM {0}".format(msg, m_split[0]))
            return bytes(m_split[0], 'utf-8')
        else:
            return msg

    def send_bot_message(self):
        counter = collections.Counter(self.message_bin)
        msg = counter.most_common(1)[0][0]
        try:
            log_info("====== SPAM TRIGGER ======".format(msg))
            log_info("{0}".format(msg))
            log_info("====== END TRIGGER ======".format(msg))
            self.queue.put_nowait(msg)
        except:
            raise

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                if self.force_reset:
                    self.force_reset = False
                    self.message_bin = []
                    self.start_time = time.time()
                end_time = time.time()
                diff = end_time - self.start_time
                if len(self.message_bin) < self.minimum_population:
                    log_info("accumulating bin {0:.2f}/seconds".format(diff))
                self.message_bin.append(self.collapse_message(msg.value))
                unique_perc = self.calculate_unique_distribution()
                if len(self.message_bin) > self.minimum_population:
                    self.message_bin.pop(0)
                    if unique_perc > self.unique_threshold:
                        self.force_reset = True
                        if diff > self.distribution_length_ms:
                            self.send_bot_message()
                self.processed += 1
            if self.stop_event.is_set():
                break



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
    parser.add_argument(
        'minimum_population', metavar='minimum_population', type=int, nargs='?',
        default=15,
        help='The minimum amount of chat messages required before kicking in.'
    )
    parser.add_argument(
        'unique_threshold', metavar='unique_threshold', type=int, nargs='?',
        default=.50,
        help='The threshold to cause a spam trigger'
    )
    parser.add_argument(
        'distribution_length_ms', metavar='distribution_length_ms', type=int, nargs='?',
        default=8,
        help='The required minimum time to trigger spam'
    )

    args = parser.parse_args()
    host = args.host
    offset = args.offset
    kafka_topic = args.kafka_topic
    minimum_population = args.minimum_population
    unique_threshold = args.unique_threshold
    distribution_length_ms = args.distribution_length_ms

    log_info("Arguments: {}".format(args))

    # The commands (spam) to send to the botKappa
    spam_message_queue = Queue()

    stop_event = threading.Event()

    # consume a kafka topic

    consumer = SpamDetectorConsumer(
        minimum_population,
        unique_threshold,
        distribution_length_ms,
        kafka_topic,
        stop_event,
        bootstrap_servers=host,
        auto_offset_reset=offset,
        queue=spam_message_queue
    )

    # waits for consumer to calculate
    bot_message_producer = TalisKafkaProducer(
        bootstrap_servers=host,
        kafka_topic=os.getenv("KAFKA_BOT_MESSAGE_TOPIC"),
        queue=spam_message_queue
    )
    bot_message_producer.setDaemon(True)

    try:
        consumer.start()
        bot_message_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
