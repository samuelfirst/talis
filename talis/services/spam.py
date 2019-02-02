'''
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated
'''
import queue
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis.kafka import SpamDetectorConsumer
from talis.kafka import DequeueProducer
from talis.processor import JsonProcessor

if __name__ == "__main__":

    # The commands (spam) to send to the botKappa
    spam_message_queue = Queue()
    stop_event = threading.Event()

    json_processor = JsonProcessor()

    # consume a kafka topic
    consumer = SpamDetectorConsumer(
        config.get('minimum_population', 10),
        config.get('unique_threshold', .4),
        config.get('distribution_length_sec', 10),
        spam_message_queue,
        stop_event,
        json_processor,
        topic=config.get('KAFKA_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'latest')
    )

    # waits for consumer to calculate
    bot_message_producer = DequeueProducer(
        spam_message_queue,
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        topic=config.get("KAFKA_BOT_MESSAGE_TOPIC")
    )
    bot_message_producer.setDaemon(True)

    try:
        consumer.start()
        bot_message_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
