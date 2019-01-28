import os
import queue
import argparse
import threading
import signal

# config and logs
from talis.config import *
from talis.log import log

# threads
from talis.kafka.queue_consumer import QueueConsumer
from talis.kafka.command_consumer import CommandConsumer
from talis.twitch_chat import TwitchChat

if __name__ == "__main__":
    config.add_oauth()
    log.info("=== Twitch Chat Producer Started ===")

    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    bot_message_consumer = QueueConsumer(
        bot_message_queue,
        stop_event,
        topic=config.get("KAFKA_BOT_MESSAGE_TOPIC"),
        auto_offset_reset="latest",
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST")
    )
    bot_message_consumer.setDaemon(True)

    # TODO: extract
    commands =  {
        '!git' : 'https://github.com/jk-',
        '!bot' : "My name is Talis and I'm a Microservice NLP AI Twitch Bot written in Python utilizing Kafka and Zookeeper. For more info type !git"
    }

    rule_based_commands = CommandConsumer(
        commands,
        bot_message_queue,
        stop_event,
        topic=config.get("KAFKA_TOPIC"),
        auto_offset_reset="latest",
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST")
    )
    rule_based_commands.setDaemon(True)

    twitch_chat_producer = TwitchChat(
        username=config.get('TWITCH_NICK'),
        oauth=config.get('TWITCH_NICK_OAUTH_TOKEN'),
        channel=config.get('TWITCH_CHANNEL'),
        queue=bot_message_queue,
        stop_event=stop_event,
        verbose=False,
        central_control=True
    )
    twitch_chat_producer.connect()

    try:
        bot_message_consumer.start()
        rule_based_commands.start()
        twitch_chat_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
