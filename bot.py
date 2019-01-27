
import os
import queue
import argparse
import threading
import signal

# config and logs
from talis.config import *
from talis.log import log

# threads
from talis.twitch_chat import TwitchChat
from talis.consumer_queue import TalisKafkaConsumerQueue

class RulesBasedKafkaProducer(TalisKafkaConsumerQueue):

    def __init__(self,
            kafka_topic,
            stop_event,
            bootstrap_servers="",
            auto_offset_reset="",
            queue=""):
        super().__init__(kafka_topic, stop_event, bootstrap_servers=bootstrap_servers, auto_offset_reset=auto_offset_reset, queue=queue)
        self.commands = {
            '!git' : 'https://github.com/jk-',
            '!bot' : "My name is Talis and I'm a Microservice NLP AI Twitch Bot written in Python utilizing Kafka and Zookeeper. For more info type !git"
        }

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                msg_d = msg.value.decode('utf-8')
                if msg_d in self.commands.keys() and self.processed < 5:
                    response = self.commands[msg_d]
                    self.queue.put_nowait(response)
                    self.processed += 1
            if self.stop_event.is_set():
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitch Message Producer')
    parser.add_argument(
        'channel', metavar='channel', type=str, nargs='?',
        default=os.getenv("CHANNEL"),
        help='The twich channel you want to join.')
    parser.add_argument(
        'host', metavar='host', type=str, nargs='?',
        default=os.getenv("KAFKA_BOOTSTRAP_HOST"),
        help='The kafka host (bootstrap)')
    parser.add_argument(
        'nick', metavar='nick', type=str, nargs='?',
        default=os.getenv("TWITCH_BOT_NICK"),
        help='The bots username/nickname on twitch')
    parser.add_argument(
        'oauth_file', metavar='oauth_file', type=str, nargs='?',
        default=os.getenv("TWITCH_BOT_OAUTH_FILE"),
        help='The path to the .oauth file')

    args = parser.parse_args()
    channel = args.channel
    host = args.host
    nick = args.nick
    oauth_file = args.oauth_file
    kafka_topic = os.getenv("KAFKA_TOPIC")

    log.info("Args: {} {}".format(args, kafka_topic))

    oauth_file_isfile = os.path.isfile(oauth_file)

    if oauth_file_isfile:
        f = open(oauth_file, 'r')
        oauth_token = f.readline().rstrip(" \n")
        f.close()
    else:
        exit("Your oauth token file doesn't exist: {}".format(oauth_file))

    log.info("=== Twitch Chat Producer Started ===")
    log.info("LOG LEVEL: {}".format(os.getenv("LOG_LEVEL")))

    bot_message_queue = queue.Queue()
    stop_event = threading.Event()

    bot_message_consumer = TalisKafkaConsumerQueue(
            os.getenv("KAFKA_BOT_MESSAGE_TOPIC"),
            stop_event,
            auto_offset_reset="latest",
            bootstrap_servers=host,
            queue=bot_message_queue
    )
    bot_message_consumer.setDaemon(True)

    rule_based_commands = RulesBasedKafkaProducer(
            os.getenv("KAFKA_TOPIC"),
            stop_event,
            auto_offset_reset="latest",
            bootstrap_servers=host,
            queue=bot_message_queue
    )
    rule_based_commands.setDaemon(True)

    twitch_chat_producer = TwitchChat(
        username=nick,
        oauth=oauth_token,
        channel=channel,
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
