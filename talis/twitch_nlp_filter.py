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
        self.chatter_level = 15
        self.last_chatter = 0
        self.message_bin = []
        self.processed = 0
        self.triggered = False
        self.question = None
        self.max_waiting_time = 90
        self.elapsed_chatter_time = 0
        self.direct_message = False
        self.from_user = None
        self.forced_chatter = False

    def trigger(self, question, forced=False):
        self.triggered = True
        self.question = question
        self.forced_chatter = forced
        log.info("Analyzing Message: {}".format(question))

    def reset(self):
        if not self.forced_chatter:
            self.message_bin = []
        self.forced_chatter = False
        self.triggered = False
        self.question = None
        self.last_chatter = time.time()
        self.elapsed_chatter_time = 0
        self.from_user = None
        self.direct_message = False

    def _get_random_message(self):
        return self.message_bin[
            random.randint(0, len(self.message_bin) - 1)
        ]

    def waiting(self):
        self.elapsed_chatter_time = time.time()
        if (
            self.elapsed_chatter_time - self.last_chatter >
            self.max_waiting_time and self.last_chatter != 0
        ):
            if len(self.message_bin):
                log.info(
                    "I've waited long enough ({:.02f}/secs). "
                    "I'm chatting.".format(
                        self.elapsed_chatter_time - self.last_chatter
                    )
                )
                self.trigger(
                    self._get_random_message(),
                    forced=True
                )

    # determines if we should be sending to chat
    def process_message(self, username, message):
        self.from_user = username
        msg = TwitchFormatter.format(message)
        if not len(msg):
            return

        at_ = re.match(r'\@(?P<username>(.+))', message)
        if at_:
            at_ = at_["username"].strip()

        now = time.time()
        self.processed += 1
        self.message_bin.append(msg)
        self.messages_sec = self.processed / (now - self.start_time)

        log.info(
            "{} in bin, {:.002f} msg/sec".format(
                len(self.message_bin),
                self.messages_sec
            )
        )

        if (
            (len(self.message_bin) >= self.chatter_level) and
            ((now - self.last_chatter) > self.chatter_level)
        ):
            self.direct_message = False
            self.trigger(self._get_random_message())
        elif at_ == config.get('TWITCH_NICK'):
            self.direct_message = True
            message = message.strip('@' + config.get('TWITCH_NICK'))
            self.trigger(message, forced=False)
