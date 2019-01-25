'''
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

def log_info(msg):
    print("AI {0}: {1}".format(consumer_name, msg))

if True:
    host = "localhost:9092"
else:
    host = os.getenv("KAFKA_BOOTSTRAP_HOST")

log_info("Connecting to {0}".format(host))

try:
    consumer = KafkaConsumer(os.getenv("KAFKA_BOT_MESSAGE_TOPIC"), bootstrap_servers=host)
    twitch_bot = TwitchChat(username=os.getenv("BOT_NAME"),
                            oauth=os.getenv("OAUTH_TOKEN"),
                            channel=os.getenv("CHANNEL"),
                            verbose=False)
except NoBrokersAvailable:
    exit("No brokers found")

log_info("Connected to {0}".format(host))

for msg in consumer:
    log_info("Received Message to send to twitch: {0}".format(msg.value))
    #twitch_bot.chatstream.send_chat_message(msg.value)
