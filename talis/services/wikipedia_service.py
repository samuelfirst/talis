"""
This AI will provide the ability for the bot to
connect to a wikipedia article and answer a question
"""
import json
import os
import queue
import re
import sys
import threading

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

import nltk
from kafka import KafkaConsumer, KafkaProducer

from talis import config, dequeue, log, push_queue, wiki_answer

if __name__ == "__main__":
    # The commands (spam) to send to the botKappa
    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    kafka_consumer = KafkaConsumer(
        config.get("KAFKA_TOPIC"),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset="latest",
    )

    kafka_producer = KafkaProducer(
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Pushes commands to the bot from the
    # bot_message_queue
    kp_thread = threading.Thread(
        target=dequeue,
        args=(kafka_producer, config.get("KAFKA_BOT_MESSAGE_TOPIC"), bot_message_queue),
        name="Kafka Chat Producer",
    )
    kp_thread.setDaemon(True)

    nltk.download("punkt")

    try:
        log.info("Starting wiki service")
        kp_thread.start()
        while not stop_event.is_set():
            for msg in kafka_consumer:
                data = json.loads(msg.value)
                message = data.get("message")

                split_message = re.findall(r"(^!q )(.+)", message)

                if split_message and len(split_message[0]) == 2:
                    split_message = split_message[0]
                    command = split_message[0].strip()
                    question = split_message[1]

                    log.info("Question: {}".format(question))

                    threading.Thread(
                        target=wiki_answer,
                        args=(
                            data,
                            question,
                            bot_message_queue,
                        ),
                        name="wiki consumer thread",
                    ).start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
