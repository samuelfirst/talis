'''
This script will attach and listen for
bot messages (temporary location for testing) and will
generate a 10 second clip of the channel where "hype" occurred
'''
import queue
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis import VideoProducer
from talis.kafka import QueueConsumer
from talis.processor import JsonProcessor

if __name__ == "__main__":
    spam_message_queue = queue.Queue()
    stop_event = threading.Event()
    json_processor = JsonProcessor()

    consumer = QueueConsumer(
        spam_message_queue,
        stop_event,
        topic=config.get('topic', config.get('KAFKA_BOT_MESSAGE_TOPIC')),
        bootstrap_servers=config.get('KAFKA_BOOTSTRAP_HOST'),
        auto_offset_reset=config.get('auto_offset_reset', 'latest')
    )

    video_producer = VideoProducer(
        spam_message_queue
    )
    video_producer.setDaemon(True)

    try:
        consumer.start()
        video_producer.start()
    except (KeyboardInterrupt, SystemExit):
        stop_event.set()
        pass
    except:
        stop_event.set()
        pass
