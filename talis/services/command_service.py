'''
Use this script to launch rule based commands
'''
import queue
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis.kafka import CommandConsumer
from talis.kafka import DequeueProducer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    # TODO: extract from commands.yml
    commands = {
        '!git': 'https://github.com/jk-',
        '!bot': (
            "My name is Talis and I'm a Microservice NLP "
            "Twitch Bot written in Python utilizing Kafka and "
            "Zookeeper. For more info type !git"
        )
    }

    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    json_processor = JsonProcessor()

    bot_message_dequeue = DequeueProducer(
        bot_message_queue,
        topic=config.get('KAFKA_BOT_MESSAGE_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST')
    )
    bot_message_dequeue.setDaemon(True)

    rule_based_commands = CommandConsumer(
        commands,
        bot_message_queue,
        stop_event,
        json_processor,
        topic=config.get("KAFKA_TOPIC"),
        auto_offset_reset="latest",
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST")
    )
    try:
        rule_based_commands.start()
        bot_message_dequeue.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        pass
    except:
        stop_event.set()
        pass
