import time
import collections
import json

from talis import log


class SpamFilter(object):

    def __init__(
        self,
        minimum_population,
        unique_threshold,
        distribution_length_ms
    ):
        self.minimum_population = minimum_population
        self.unique_threshold = unique_threshold
        self.distribution_length_ms = distribution_length_ms
        self.message_bin = []
        self.start_time = time.time()
        self.triggered = False
        self.message = None

    def calculate_unique_distribution(self):
        bin_len = len(self.message_bin)
        counter = collections.Counter(
            map(lambda x: x.lower(), self.message_bin)
        )
        most_common_count = counter.most_common(1)[0][1]
        r = most_common_count / bin_len
        log.info("{0:.2f}% of {1:.2f}% threshold".format(
            r * 100,
            self.unique_threshold * 100
        ))
        return r

    def collapse_message(self, msg):
        m_split = msg.lower().split(" ")
        bin_len = len(m_split)
        unique = len(list(set(map(lambda x: x.lower(), m_split))))
        if bin_len > 1 and unique == 1:
            log.info("DUPLICATE SPAM {0}".format(msg, m_split[0]))
            return m_split[0]
        else:
            return msg

    def reset(self):
        self.triggered = False
        self.message_bin = []
        self.message = None
        self.start_time = time.time()

    def process_spam(self, message):
        end_time = time.time()
        diff = end_time - self.start_time
        if len(self.message_bin) < self.minimum_population:
            log.info("accumulating bin {0:.2f}/seconds".format(diff))
        self.message_bin.append(
            self.collapse_message(message)
        )
        unique_perc = self.calculate_unique_distribution()
        if len(self.message_bin) > self.minimum_population:
            self.message_bin.pop(0)
            if unique_perc > self.unique_threshold:
                if diff > self.distribution_length_ms:
                    self.triggered = True
                    self.set_message()

    def set_message(self):
        counter = collections.Counter(self.message_bin)
        self.message = counter.most_common(1)[0][0]
        log.info("====== SPAM TRIGGER ======")
        log.info("{0}".format(self.message))
        log.info("====== END TRIGGER ======")
