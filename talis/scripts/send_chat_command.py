'''
user this script to send a bot command
'''
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log

from kafka import KafkaProducer
from kafka import KafkaConsumer
from talis import twitch_schema

if __name__ == "__main__":

    try:
        while True:
            command = input("What Message?\n")
            kafka_topic = config.get("KAFKA_BOT_MESSAGE_TOPIC")

            kafka_producer = KafkaProducer(
                bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            data = twitch_schema.as_dict(
                config.get('TWITCH_CHANNEL'),
                command
            )

            kafka_producer.send(kafka_topic, data)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        raise
