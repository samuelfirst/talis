'''
Use this script to debug a kafka topic.
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis.config import config
from talis.log import log
from talis.kafka.stdout_consumer import StdoutConsumer

if __name__ == "__main__":
    try:
        consumer = StdoutConsumer(
            topic=config.get('topic'),
            bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
            auto_offset_reset=config.get('auto_offset_reset', 'latest')
        )
        consumer.start()
    except:
        exit(".\n")
