'''
Use this script to debug a kafka topic.
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis import config
from talis import log
from talis.kafka import StdoutConsumer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    consumer = StdoutConsumer(
        JsonProcessor(),
        topic=config.get('topic', config.get('KAFKA_TOPIC')),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'earliest')
    )
    try:
        consumer.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    except:
        pass
