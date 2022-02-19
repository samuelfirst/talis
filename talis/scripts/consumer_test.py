"""
Use this script to debug a kafka topic.
"""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from kafka import KafkaConsumer

from talis import config, log

if __name__ == "__main__":

    kafka_consumer = KafkaConsumer(
        config.get("topic", config.get("KAFKA_TOPIC")),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset=config.get("auto_offset_reset", "latest"),
    )

    for msg in kafka_consumer:
        data = json.loads(msg.value)
        print(msg)
