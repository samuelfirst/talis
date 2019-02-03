'''
This AI will provide the ability for the bot to
connect to a wikipedia article and answer a question
'''
import queue
import threading
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis import push_queue
from talis import dequeue
from talis import twitch_schema
from talis import twitch_answer
from talis import TwitchNLPFilter

from kafka import KafkaConsumer
from kafka import KafkaProducer

if __name__ == "__main__":
    # The commands (spam) to send to the botKappa
    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    kafka_consumer = KafkaConsumer(
        config.get("KAFKA_TOPIC"),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset="latest"
    )

    kafka_producer = KafkaProducer(
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Pushes commands to the bot from the
    # bot_message_queue
    kp_thread = threading.Thread(
        target=dequeue,
        args=(
            kafka_producer,
            config.get('KAFKA_BOT_MESSAGE_TOPIC'),
            bot_message_queue
        ),
        name="Kafka Chat Producer"
    )
    kp_thread.setDaemon(True)

    try:
        kp_thread.start()
        twitch_nlp = TwitchNLPFilter()
        while not stop_event.is_set():
            for msg in kafka_consumer:
                data = json.loads(msg.value)
                message = data.get('message')
                twitch_nlp.process_message(message)
                if twitch_nlp.triggered:
                    threading.Thread(
                        target=twitch_answer,
                        args=(data, twitch_nlp.question, bot_message_queue,),
                        name="twitch answer thread"
                    ).start()
                    twitch_nlp.reset()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
