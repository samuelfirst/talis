'''
This producer will join a twitch IRC CHANNEL
${CHANNEL} and pipe the messages to kafka
on ${KAFKA_TOPIC}
'''
from __future__ import print_function

from talis.config import *
from talis.log import log
from talis.twitch_chat import TwitchChat

from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable

import time
import sys
import os

is_consumer = False

if __name__ == "__main__":
    log.info("=== Bot Started ===")
    log.info("LOG LEVEL: {}".format(os.getenv("LOG_LEVEL")))

    if is_consumer:
        (channel, host) = sys.argv[1:]
    else:
        channel = os.getenv("CHANNEL")
        host = os.getenv("KAFKA_BOOTSTRAP_HOST")

    producer = KafkaProducer(bootstrap_servers=host)
    log.info("REGISTERING as PRODUCER: {}".format(os.getenv("KAFKA_BOOTSTRAP_HOST")))

    log.info("Joining Channel {} as {}".format(os.getenv("CHANNEL"), os.getenv("TWTICH_CONSUMER_NICK")))
    with TwitchChat(username=os.getenv("TWTICH_CONSUMER_NICK"),
                          oauth=os.getenv("TWTICH_CONSUMER_NICK_OAUTH_TOKEN"),
                          channel=channel,
                          verbose=False) as chatstream:
        try:
            while True:
                received = chatstream.twitch_receive_messages()
                if received:
                    username = received[0]["username"]
                    msg = received[0]["message"]
                    try:
                        log.info("{0}: {1}".format(username, msg))
                        producer.send(os.getenv("KAFKA_TOPIC"), bytes(msg, 'utf-8'))
                    except NoBrokersAvailable as e:
                        log.info(e)
                        exit()
        except KeyboardInterrupt:
            log.info("Goodbye\n")
