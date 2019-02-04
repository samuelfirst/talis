import threading
import time
import random
import re

from talis import config
from talis import log

from talis.twitch_formatter import TwitchFormatter

class TwitchNLPFilter(object):
    '''
        TODO: Clean up this class. It was for getting
        out a quick demo of wikipedia interaction.
    '''
    def __init__(self):
        self.seen_messages = 0
        self.start_time = time.time()
        self.messages_sec = 0
        self.chatter_level = 8
        self.last_chatter = 0
        self.accuracy = 3
        self.message_bin = []
        self.processed = 0
        self.triggered = False
        self.question = None

    def trigger(self, question):
        self.triggered = True
        self.question = question
        log.info("Got question {}".format(question))

    def reset(self):
        self.message_bin = []
        self.triggered = False
        self.question = None
        self.last_chatter = time.time()

    # determines if we should be sending to chat
    def process_message(self, message):
        msg = TwitchFormatter.format(message)
        if not len(msg):
            return

        at_ = re.match(r'\@(?P<username>(.+? ))', message)
        if at_:
            at_ = at_["username"].strip()

        now = time.time()
        self.processed += 1
        self.message_bin.append(msg)
        self.messages_sec = self.processed / (now - self.start_time)

        #log.info("{} processed {} time".format(self.processed, now - self.start_time))
        log.info("{} msg/sec".format(self.messages_sec))

        if (
            (len(self.message_bin) >= self.chatter_level) and
            ((now - self.last_chatter) > self.chatter_level)
        ):
            self.trigger(self.message_bin[self.chatter_level - self.accuracy])
        elif at_ == config.get('TWITCH_NICK'):
            self.trigger(message.strip('@' + config.get('TWITCH_NICK')))
