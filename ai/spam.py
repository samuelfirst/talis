'''
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated

Actually a Host Giveway "Feature"

'''
import time
import collections

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis.config import *
from talis.log import log

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

consumer_name = "spam"
distribution_length_ms = 10
minimum_population = 20
unique_threshold = .80
kafka_offset = "end"

def log_info(msg):
    print("AI {0}: {1}".format(consumer_name, msg))

if True:
    host = "localhost:9092"
else:
    host = os.getenv("KAFKA_BOOTSTRAP_HOST")

log_info("Connecting to {0}".format(host))

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"), bootstrap_servers=host)
    producer = KafkaProducer(bootstrap_servers=host)
except NoBrokersAvailable:
    exit("No brokers found")
except:
    pass

message_bin = []
start_time = time.time()

forceReset = False

def calculate_unique_distribution():

    bin_len = len(message_bin)
    counter = collections.Counter(map(lambda x : x.lower(), message_bin))
    most_common_count = counter.most_common(1)[0][1]
    r = most_common_count/bin_len
    log_info("{0:.2f}% of {1:.2f}% threshold".format(r*100, unique_threshold*100))

    return r

def collapse_message(msg):
    m_split = msg.decode('utf-8').lower().split(" ")
    bin_len = len(m_split)
    unique = len(list(set(map(lambda x : x.lower(),m_split))))
    if bin_len > 1 and unique == 1:
        log_info("DUPLICATE SPAM {0}".format(msg, m_split[0]))
        return bytes(m_split[0], 'utf-8')
    else:
        return msg

def send_bot_message():
    counter = collections.Counter(message_bin)
    msg = counter.most_common(1)[0][0]
    try:
        log_info("====== SPAM TRIGGER ======".format(msg))
        log_info("{0}".format(msg))
        log_info("====== END TRIGGER ======".format(msg))
        producer.send(os.getenv("KAFKA_BOT_MESSAGE_TOPIC"), msg)
    except:
        exit("Something happened.")

for msg in consumer:
    if forceReset:
        forceReset = False
        start_time = time.time()
        message_bin = []
    end_time = time.time()
    diff = end_time - start_time
    if len(message_bin) < minimum_population:
        log_info("accumulating bin {0:.2f}/seconds".format(diff))
    message_bin.append(collapse_message(msg.value))
    unique_perc = calculate_unique_distribution()
    if len(message_bin) > minimum_population:
        message_bin.pop(0)
        if unique_perc > unique_threshold:
            forceReset = True
            if diff > distribution_length_ms:
                send_bot_message()
