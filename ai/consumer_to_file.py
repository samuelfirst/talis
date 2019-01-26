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

with open('./data/twitch_messages.txt', 'w') as filehandle:
    for msg in consumer:
        filehandle.write(msg.value.decode('utf-8')+"\r\n")

f.close()
