'''
This chat message consumer will test the connection
of kafka and subscribe to the kafka topic.
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis.config import *
from talis.log import log

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"), bootstrap_servers="localhost:9092")
except NoBrokersAvailable:
    exit("No brokers found")
except:
    pass

for msg in consumer:
    print(msg)
