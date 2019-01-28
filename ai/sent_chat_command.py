'''
user this script to send a bot command
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import argparse

from talis.config import *
from talis.log import log

from kafka import KafkaProducer

if __name__ == "__main__":

    try:
        while True:
            command = input("What command?\n")
            kafka_topic = config.get("KAFKA_BOT_MESSAGE_TOPIC")

            producer = KafkaProducer(bootstrap_servers="localhost:9092")
            producer.send(kafka_topic, bytes(command, 'utf-8'))
            producer.flush()
    except (KeyboardInterrupt, SystemExit):
        pass
    except:
        pass
