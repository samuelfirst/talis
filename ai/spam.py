'''
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
import threading

from queue import Queue

from talis.config import config
from talis.log import log

from talis.kafka.spam_detector_consumer import SpamDetectorConsumer
from talis.kafka.dequeue_producer import DequeueProducer

if __name__ == "__main__":
    log_info("Arguments: {}".format(args))

    # The commands (spam) to send to the botKappa
    spam_message_queue = Queue()
    stop_event = threading.Event()

    # consume a kafka topic
    consumer = SpamDetectorConsumer(
        config.get('minimum_population'),
        config.get('unique_threshold'),
        config.get('distribution_length_ms'),
        spam_message_queue,
        stop_even,
        topic=config.get('KAFKA_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset')
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
