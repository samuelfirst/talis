
from talis.config import *
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import os

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"), bootstrap_servers="localhost:9092")
except NoBrokersAvailable:
    exit("No brokers found")

for msg in consumer:
    print(msg)
