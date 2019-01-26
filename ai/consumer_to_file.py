'''
Saves the twitch_messages Kafka topic to a txt file
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis.config import *
from talis.log import log

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"), bootstrap_servers="localhost:9092",
    consumer_timeout_ms=400)
    consumer.topics()
    consumer.seek_to_beginning()
except NoBrokersAvailable:
    exit("No brokers found")
except:
    pass

f = open('./data/twitch_messages.txt','wr', errors = 'ignore')

for msg in consumer:
    f.write(msg.value)

f.close()
