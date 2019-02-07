import queue
import threading
import json

from talis import config
from talis import log
from talis import push_queue
from talis import dequeue
from talis import TwitchChat

from kafka import KafkaConsumer
from kafka import KafkaProducer


if __name__ == "__main__":
    config.add_oauth()
    log.setLevel(config.log_level())
    log.info("=== Twitch Bot Started ===")


    print(config.get("KAFKA_BOOTSTRAP_HOST"))

    chat_queue = queue.Queue()
    bot_message_queue = queue.Queue()
    admin_command_queue = queue.Queue()
    stop_event = threading.Event()

    kafka_consumer = KafkaConsumer(
        config.get("KAFKA_BOT_MESSAGE_TOPIC"),
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset="latest"
    )

    admin_kafka_consumer = KafkaConsumer(
        "central_control",
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        auto_offset_reset="latest"
    )

    kafka_producer = KafkaProducer(
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    kc_thread = threading.Thread(
        target=push_queue,
        args=(kafka_consumer, bot_message_queue, stop_event),
        name="Kafka Bot Message Consumer"
    )

    admin_kc_thread = threading.Thread(
        target=push_queue,
        args=(admin_kafka_consumer, admin_command_queue, stop_event),
        name="Kafka Central Control"
    )

    kp_thread = threading.Thread(
        target=dequeue,
        args=(kafka_producer, config.get('KAFKA_TOPIC'), chat_queue),
        name="Kafka Chat Producer"
    )

    twitch_chat_producer = TwitchChat(
        config.get('TWITCH_NICK'),
        config.get('TWITCH_OAUTH_TOKEN'),
        config.get('TWITCH_CHANNEL'),
        chat_queue,
        bot_message_queue,
        admin_command_queue,
        stop_event
    )
    twitch_chat_producer.connect()

    if config.get('channels'):
        for i in config.get('channels'):
            twitch_chat_producer.join_channel(i)

    try:
        twitch_chat_producer.start()
        admin_kc_thread.start()
        kc_thread.start()
        kp_thread.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        pass
    except:
        stop_event.set()
        pass
