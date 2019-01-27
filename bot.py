'''

NOTE: The twitch chat is pushing messages to kafka, but should only do it when it's a producer
This bot should just be a listener on twitch chat, but not pipe messages

TODO:
    + thread consumer
    + thread bot

This consumer will join a twitch IRC CHANNEL
${CHANNEL} and send commands that are piped
to ${KAFKA_BOT_MESSAGE_TOPIC}
'''

from talis.config import *
from talis.log import log
from talis.twitch_chat import TwitchChat

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

consumer_name = "BOT"

sent_messages = 0
max_messages = 8

def log_info(msg):
    print("AI {0}: {1}".format(consumer_name, msg))

if True:
    host = "localhost:9092"
else:
    host = os.getenv("KAFKA_BOOTSTRAP_HOST")

log_info("Connecting to Kafka on: {0}".format(host))

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_BOT_MESSAGE_TOPIC"),
                            bootstrap_servers=host,
                            consumer_timeout_ms=400)
except NoBrokersAvailable:
    exit("No brokers found")

log_info("Connected to {0}".format(host))

with TwitchChat(username=os.getenv("TWITCH_BOT_NICK"),
                oauth=os.getenv("TWITCH_BOT_OAUTH_TOKEN"),
                channel=os.getenv("CHANNEL"),
                verbose=False) as chatstream:
    try:
        while True:
            received = chatstream.twitch_receive_messages()

            for msg in consumer:
                log_info("Received Message to send to twitch: {0}".format(msg.value))
                if sent_messages > max_messages:
                    exit("Sent too many messages {0}".format(sent_messages))
                sent_messages += 1
                chatstream.send_chat_message(msg.value.decode('utf-8'))
                break
    except KeyboardInterrupt:
        log.info("Goodbye\n")
