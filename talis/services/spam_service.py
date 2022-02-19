"""
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated
"""
import json
import os
import queue
import sys
import threading

from kafka import KafkaConsumer, KafkaProducer

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import SpamFilter, config, dequeue, log, push_queue, TwitchSchema

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

    try:
        kp_thread.start()

        spam = SpamFilter(
            config.get("minimum_population", 4),
            config.get("unique_threshold", 0.5),
            config.get("distribution_length_sec", 1),
        )

        while not stop_event.is_set():
            for msg in kafka_consumer:
                data = json.loads(msg.value)
                message = data.get("message")
                log.info("Got latest message {}".format(message))
                spam.process_spam(message)
                if spam.triggered:
                    log.info("Found spam")
                    send_to_bot = TwitchSchema.as_dict(
                        data.get("channel"), spam.message
                    )
                    bot_message_queue.put_nowait(send_to_bot)
                    spam.reset()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise
