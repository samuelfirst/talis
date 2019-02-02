'''
user this script to send a bot command
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from kafka import KafkaProducer

from talis import config
from talis import log
from talis.formatter import JsonFormatter

if __name__ == "__main__":

    json_formatter = JsonFormatter()
    try:
        while True:
            command = input("What command?\n")
            kafka_topic = config.get("KAFKA_BOT_MESSAGE_TOPIC")
            # todo: format
            data = {
                'channel': config.get('TWITCH_CHANNEL'),
                'message': command
            }
            producer = KafkaProducer(bootstrap_servers="localhost:9092")
            producer.send(
                kafka_topic,
                bytes(json_formatter.format(data), 'utf-8')
            )
            producer.flush()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        raise
