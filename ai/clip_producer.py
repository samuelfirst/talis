'''
This script will attach and listen for 
bot messages (temporary location for testing) and will
generate a 10 second clip of the channel where "hype" occurred
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import threading

from queue import Queue

from talis.config import config
from talis.log import log

from talis.kafka.queue_consumer import QueueConsumer
from talis.video_producer import VideoProducer

if __name__ == "__main__":
    try:
        spam_message_queue = Queue()
        stop_event = threading.Event()

        consumer = QueueConsumer(
            spam_message_queue,
            stop_event,
            topic=config.get('topic', config.get('KAFKA_BOT_MESSAGE_TOPIC')),
            bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
            auto_offset_reset=config.get('auto_offset_reset', 'latest')
        )
        consumer.start()
        video_producer = VideoProducer(
            spam_message_queue
        )
        video_producer.setDaemon(True)
        video_producer.start()
    except:
        stop_event.set()
        raise
