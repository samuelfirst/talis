
from .talis.config import *
from .talis.log import log
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

from talis import TwitchChat

import os
import time
import collections

consumer_name = "Spam"
distribution_length_ms = 10000
minimum_population = 40
unique_threshold = .40
kafka_offset = "end"

def log_info(msg):
    return "AI {0}: {1}".format(consumer_name, msg)

if test:
    host = "localhost:9092"
else:
    host = os.getenv("KAFKA_BOOTSTRAP_HOST")

log_info("Connecting to {0}".format(host))

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"), bootstrap_servers=host)
    producer = KafkaProducer(bootstrap_servers=host)
except NoBrokersAvailable:
    exit("No brokers found")

'''
ConsumerRecord(
    topic='twitch_messages', p
    artition=0,
    offset=614,
    timestamp=1548405448730,
    timestamp_type=0,
    key=None,
    value=b'they might of had it n were doing miles',
    headers=[],
    checksum=394727164,
    serialized_key_size=-1,
    serialized_value_size=39,
    serialized_header_size=-1
)
'''

message_bin = []

start_time = time.time()

def calculates_unique_distribution():
    bin_len = len(message_bin)
    unique = len(list(set(message_bin)))

    return unique_perc = unique//bin_len

def send_bot_message():
    counter=collections.Counter(message_bin)
    msg = counter.most_common(1)[0][0]
    try:
        log_info("Sending message to bot {0}".format(msg))
        producer.send(os.getenv("KAFKA_BOT_MESSAGE_TOPIC"), msg)
    except:
        exit("Something happened.")

for msg in consumer:
    message_bin.append(msg.value)
    end_time = time.time()
    diff = end_time - start_time
    log_info("Time difference {0}".format(diff))
    if len(message_bin) > minimum_population:
        message_bin.pop(0)
        unique_perc = calculates_unique_distribution()
        if unique_perc > unique_threshold:
            send_bot_message()
