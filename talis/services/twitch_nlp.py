'''
This AI will provide the ability for the bot to
connect to a wikipedia article and answer a question
'''
import queue
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis.kafka import WikiConsumer
from talis.kafka import DequeueProducer
from talis.kafka import TwitchNLP
from talis.processor import JsonProcessor

if __name__ == "__main__":
    # The commands (spam) to send to the botKappa
    chat_queue = queue.Queue()
    stop_event = threading.Event()
    json_processor = JsonProcessor()

    file = open('data/twitch_doc.txt', 'r')
    twitch_doc = file.read().split("\n")
    file.close()

    # consume a kafka topic
    twitch_nlp = TwitchNLP(
        chat_queue,
        stop_event,
        json_processor,
        topic=config.get('KAFKA_TOPIC'),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'latest')
    )
    twitch_nlp.algo.subject = "twitch"
    twitch_nlp.algo.set_doc(twitch_doc)

    # waits for consumer to calculate
    bot_message_producer = DequeueProducer(
        chat_queue,
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        topic=config.get("KAFKA_BOT_MESSAGE_TOPIC")
    )
    bot_message_producer.setDaemon(True)

    try:
        twitch_nlp.start()
        bot_message_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
