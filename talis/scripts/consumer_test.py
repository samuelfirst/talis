'''
Use this script to debug a kafka topic.
'''
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
        auto_offset_reset=config.get('auto_offset_reset', 'latest')
    )

    for msg in kafka_consumer:
        data = json.loads(msg.value)
        message = data.get('message')
        print(f"{message}")
