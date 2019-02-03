'''
Use this script to create a twitch doc
for nlp processing
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis.formatter import TwitchFormatter

from kafka import KafkaConsumer

if __name__ == "__main__":
    print(config.get('KAFKA_TOPIC'))

    twitch_formatter = TwitchFormatter()

    consumer = KafkaConsumer(
        config.get('KAFKA_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'earliest'),
        consumer_timeout_ms=1000
    )

    with open('data/twitch_doc.txt', 'w') as fh:
        for msg in consumer:
            data = json.loads(msg.value)
            message = data.get('message')
            formatted = twitch_formatter.format(message)
            if len(formatted):
                fh.write(formatted + "\n")
        fh.close()
