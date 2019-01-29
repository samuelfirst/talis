import time
import collections
import json

from talis import log
from talis.kafka import QueueConsumer

# fix
def log_info(msg):
    print("AI SPAM: {}".format(msg))

class SpamDetectorConsumer(QueueConsumer):
    def __init__(self, minimum_population, unique_threshold, distribution_length_ms,
            queue, stop_event, data_processor, *args, **kwargs):
        super().__init__(queue, stop_event, data_processor, *args, **kwargs)
        self.message_bin = []
        self.data_bin = []
        self.minimum_population = minimum_population
        self.unique_threshold = unique_threshold
        self.distribution_length_ms = distribution_length_ms
        self.force_reset = False
        self.start_time = time.time()

    def calculate_unique_distribution(self):

        bin_len = len(self.message_bin)
        counter = collections.Counter(map(lambda x : x.lower(), self.message_bin))
        most_common_count = counter.most_common(1)[0][1]
        r = most_common_count/bin_len
        log_info("{0:.2f}% of {1:.2f}% threshold".format(r*100, self.unique_threshold*100))
        return r

    def collapse_message(self, msg):
        m_split = msg.lower().split(" ")
        bin_len = len(m_split)
        unique = len(list(set(map(lambda x : x.lower(),m_split))))
        if bin_len > 1 and unique == 1:
            log_info("DUPLICATE SPAM {0}".format(msg, m_split[0]))
            return m_split[0]
        else:
            return msg

    def send_bot_message(self):
        counter = collections.Counter(self.message_bin)
        msg = counter.most_common(1)[0][0]
        data = {
            'channel' : self.data_bin[0].get('channel'),
            'message' : msg
        }
        data_json = json.dumps(data)
        try:
            log_info("====== SPAM TRIGGER ======".format(msg))
            log_info("{0}".format(data_json))
            log_info("====== END TRIGGER ======".format(msg))
            self.queue.put_nowait(bytes(data_json, 'utf-8'))
        except:
            raise

    def run(self):
        while not self.stop_event.is_set():
            for msg in self.consumer:
                data = json.loads(msg.value)
                if self.force_reset:
                    self.force_reset = False
                    self.message_bin = []
                    self.data_bin = []
                    self.start_time = time.time()
                end_time = time.time()
                diff = end_time - self.start_time
                if len(self.message_bin) < self.minimum_population:
                    log_info("accumulating bin {0:.2f}/seconds".format(diff))
                self.message_bin.append(self.collapse_message(data.get('message')))
                self.data_bin.append(data)
                unique_perc = self.calculate_unique_distribution()
                if len(self.message_bin) > self.minimum_population:
                    self.message_bin.pop(0)
                    self.data_bin.pop(0)
                    if unique_perc > self.unique_threshold:
                        self.force_reset = True
                        if diff > self.distribution_length_ms:
                            self.send_bot_message()
                self.processed += 1
            if self.stop_event.is_set():
                break
