'''
Output a kafka topic to a file
# TODO: Add compression
# TODO: Add customer arg
'''
import queue
import threading
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log

from kafka import KafkaConsumer

if __name__ == "__main__":

    kafka_consumer = KafkaConsumer(
        config.get("KAFKA_TOPIC"),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset='earliest',
        consumer_timeout_ms=300
    )

    with open('data/kafka_output.txt', 'w') as file:
        for msg in kafka_consumer:
            data = json.loads(msg.value)
            message = data.get('message')
            file.write(f"{message}\n")
