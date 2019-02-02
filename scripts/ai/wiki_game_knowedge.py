'''
This AI will provide the ability for the bot to
connect to a wikipedia article and answer a question
'''
import os
import sys
import time
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from queue import Queue

from talis import config
from talis import log
from talis.kafka import WikiConsumer
from talis.kafka import DequeueProducer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    # The commands (spam) to send to the botKappa
    chat_queue = Queue()
    stop_event = threading.Event()
    json_processor = JsonProcessor()

    # consume a kafka topic
    consumer = WikiConsumer(
        chat_queue,
        stop_event,
        json_processor,
        topic=config.get('KAFKA_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'latest')
    )

    # waits for consumer to calculate
    bot_message_producer = DequeueProducer(
        chat_queue,
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
