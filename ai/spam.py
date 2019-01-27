'''
This chat message consumer will make the bot more
cancerous by participating in events where spam
becomes highly concentrated

Actually a Host Giveway "Feature"

'''
'''
Use this script to debug a kafka topic.
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import argparse
import threading
import collections

from talis.config import *
from talis.log import log
from talis.consumer_queue import TalisConsumerQueue

class SpamDetector(TalisKafkaConsumer):

    '''
    Original script used a global list
    and now we have "queue" to facilitate threading
    so the idea of "processing" the queue doesnt hold
    '''

    def calculate_unique_distribution(self):

        '''
        bin_len = len(message_bin)
        counter = collections.Counter(map(lambda x : x.lower(), message_bin))
        most_common_count = counter.most_common(1)[0][1]
        r = most_common_count/bin_len
        log_info("{0:.2f}% of {1:.2f}% threshold".format(r*100, unique_threshold*100))
        '''
        return r

    def collapse_message(self, msg):
        m_split = msg.decode('utf-8').lower().split(" ")
        bin_len = len(m_split)
        unique = len(list(set(map(lambda x : x.lower(),m_split))))
        if bin_len > 1 and unique == 1:
            log_info("DUPLICATE SPAM {0}".format(msg, m_split[0]))
            return bytes(m_split[0], 'utf-8')
        else:
            return msg

    def send_bot_message(self):
        counter = collections.Counter(message_bin)
        msg = counter.most_common(1)[0][0]
        try:
            log_info("====== SPAM TRIGGER ======".format(msg))
            log_info("{0}".format(msg))
            log_info("====== END TRIGGER ======".format(msg))
            producer.send(os.getenv("KAFKA_BOT_MESSAGE_TOPIC"), msg)
        except:
            exit("Something happened.")

    def run(self):
        '''

        LEFT OFF HERE!!


        self.queue.gsize() docs say itts an "approx"
        maight have to use as standard array?

        Tthinkiing way too complicated

        Consumer shoudl loop through message from latest Kafka log
        and pip a message to the producer bot
    
        '''
        while not self.stop_event.is_set():

            received = self.twitch_receive_messages()
            if received:
                username = received[0]["username"]
                msg = received[0]["message"]
                try:
                    if self.verbose:
                        log.info("{0}: {1}".format(username, msg))
                    self.queue.put_nowait(bytes(msg, 'utf-8'))
                except:
                    log.info(e)
                    self.close()


        for msg in self.consumer:
            if forceReset:
                forceReset = False
                start_time = time.time()
                message_bin = []
            end_time = time.time()
            diff = end_time - start_time
            if len(message_bin) < minimum_population:
                log_info("accumulating bin {0:.2f}/seconds".format(diff))
            message_bin.append(self.collapse_message(msg.value))
            unique_perc = self.calculate_unique_distribution()
            if len(message_bin) > minimum_population:
                message_bin.pop(0)
                if unique_perc > unique_threshold:
                    forceReset = True
                    if diff > distribution_length_ms:
                        self.send_bot_message()
            self.processed += 1
            if self.stop_event.is_set():
                break

def log_info(msg):
    print("AI {0}: {1}".format(consumer_name, msg))

if __name__ == "__main__":
    consumer_name = "SPAM"
    #distribution_length_ms = 10

    parser = argparse.ArgumentParser(description='Debug a kafka topic')
    parser.add_argument(
        'host', metavar='host', type=str, nargs='?',
        default=os.getenv("KAFKA_BOOTSTRAP_HOST"),
        help='The kafka host (bootstrap)'
    )
    parser.add_argument(
        'offset', metavar='offset', type=str, nargs='?',
        default='latest',
        help='The offset of the kafka offset to start from (latest|earliest)'
    )
    parser.add_argument(
        'kafka_topic', metavar='kafka_topic', type=str, nargs='?',
        default=os.getenv("KAFKA_TOPIC"),
        help='The kafka topic you want to debug'
    )
    parser.add_argument(
        'minimum_population', metavar='minimum_population', type=int, nargs='?',
        default=20,
        help='The minimum amount of chat messages required before kicking in.'
    )
    parser.add_argument(
        'unique_threshold', metavar='unique_threshold', type=int, nargs='?',
        default=.50,
        help='The threshold to cause a spam trigger'
    )

    args = parser.parse_args()
    host = args.host
    offset = args.offset
    kafka_topic = args.kafka_topic
    minimum_population = args.minimum_population
    unique_threshold = args.unique_threshold

    log.info("Arguments: {}".format(args))


    chat_queue = queue.Queue()

    consumer_stop_event = threading.Event()
    producer_stop_event = threading.Event()


    consumer = TalisConsumerQueue(os.getenv("KAFKA_TOPIC"), bootstrap_servers=host)




    spam_consumer = TalisKafkaProducer(bootstrap_servers=host, kafka_topic=kafka_topic, queue=chat_queue)
    twitch_chat_consumer.setDaemon(True)

    twitch_chat_producer = TwitchChat(username=nick, oauth=oauth_token, channel=channel,
                                    queue=chat_queue, stop_event=stop_event, verbose=True)
    twitch_chat_producer.connect()


    Consume from KafkaConsumer
        pipe data into queue
    Producer from SpamDetector
        get from queue

    try:
        twitch_chat_consumer.start()
        twitch_chat_producer.start()
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        raise
    except:
        stop_event.set()
        raise

    try:

        producer = KafkaProducer(bootstrap_servers=host)
        consumer.start()
    except:
        consumer_stop_event.set()
        raise
