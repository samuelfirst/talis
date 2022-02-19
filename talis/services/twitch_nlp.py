"""
This AI will provide the ability for the bot to
connect to a wikipedia article and answer a question
"""
import json
import os
import queue
import sys
import threading

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from kafka import KafkaConsumer, KafkaProducer

from talis import (TwitchNLPFilter, config, dequeue, log, nlp_answer,
                   push_queue, TwitchSchema)

if __name__ == "__main__":
    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    kafka_consumer = KafkaConsumer(
        config.get("KAFKA_TOPIC"),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset="latest",
        consumer_timeout_ms=300,
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

    try:
        kp_thread.start()
        twitch_nlp = TwitchNLPFilter()

        log.info("===Started NLP===")
        while not stop_event.is_set():
            twitch_nlp.waiting()
            data = None

            for msg in kafka_consumer:
                data = json.loads(msg.value)
                username = data.get("username")
                message = data.get("message")
                twitch_nlp.process_message(username, message)

            # we have no way of dynamically updating
            # the channel with the :join: channel.. yet
            if not data:
                data = TwitchSchema.as_dict(config.get("TWITCH_CHANNEL"), None)

            if twitch_nlp.triggered:
                threading.Thread(
                    target=nlp_answer,
                    args=(
                        data,
                        twitch_nlp.question,
                        bot_message_queue,
                        config.get('doc-file', 'nlp_docs/twitch_doc.txt'),
                    ),
                    name="twitch answer thread",
                ).start()
                twitch_nlp.reset()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
