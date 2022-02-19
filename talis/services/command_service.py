"""
Use this script to launch rule based commands
"""
import json
import os
import queue
import sys
import threading

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from kafka import KafkaConsumer, KafkaProducer

from talis import config, dequeue, log, push_queue, TwitchSchema

if __name__ == "__main__":
    # TODO: extract from commands.yml
    commands = {
        "!git": "https://github.com/jk-",
        "!bot": (
            "My name is Talis and I'm a Microservice NLP "
            "Twitch Bot written in Python utilizing Kafka and "
            "Zookeeper. For more info type !git"
        ),
    }

    chat_queue = queue.Queue()
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
        log.info("Starting command service")
        kp_thread.start()
        while not stop_event.is_set():
            for msg in kafka_consumer:
                data = json.loads(msg.value)
                command = data.get("message")
                log.info("Got latest message {}".format(command))
                if command in commands.keys():
                    log.info("Found comand")
                    response = commands[command]
                    send_to_bot = TwitchSchema.as_dict(data.get("channel"), response)
                    bot_message_queue.put_nowait(send_to_bot)

    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        pass
    except:
        stop_event.set()
        raise
