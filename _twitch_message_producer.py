'''
Use bot.py for entry bot. DEPRECATED
'''
import os
import queue
import argparse
import threading
import signal

# config and logs
from talis.config import config
from talis.log import log

# threads
from talis.twitch_chat import TwitchChat
from talis.kafka.dequeue_producer import DequeueProducer

if __name__ == "__main__":
    config.add_oauth()

    log.info("=== Twitch Chat Producer Started ===")

    chat_queue = queue.Queue()
    stop_event = threading.Event()

    twitch_chat_consumer = DequeueProducer(
        chat_queue,
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        topic=config.get('KAFKA_TOPIC')
    )
    twitch_chat_consumer.setDaemon(True)

    twitch_chat_producer = TwitchChat(
        username=config.get('TWITCH_NICK'),
        oauth=config.get('TWITCH_NICK_OAUTH_TOKEN'),
        channel=config.get('TWITCH_CHANNEL'),
        verbose=config.get('v'),
        queue=chat_queue,
        stop_event=stop_event
    )
    twitch_chat_producer.connect()

    try:
        twitch_chat_consumer.start()
        twitch_chat_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
