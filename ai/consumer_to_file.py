'''
Output a kafka topic to a file
# TODO: Add compression
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from talis import config
from talis import log
from talis.kafka import FileConsumer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    log.info("Arguments: {}".format(args))

    consumer_stop_event = threading.Event()

    try:
        consumer = FileConsumer(
            consumer_stop_event,
            JsonProcessor(),
            topic=config.get('topic'),
            bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
            auto_offset_reset=config.get('auto_offset_reset')
        )
        consumer.start()
    except:
        consumer_stop_event.set()
        raise
