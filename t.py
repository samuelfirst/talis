
import threading
import queue

from talis.kafka.consumer import TalisConsumer
from talis.kafka.queue_consumer import QueueConsumer
from talis.kafka.command_consumer import CommandConsumer


if __name__ == "__main__":
    stop_event = threading.Event()
    q = queue.Queue()


    queueconsumer = TalisConsumer.from_threaded(q, stop_event, topic="tada")
    queueconsumer.start()

    queueconsumer = QueueConsumer(q, stop_event, topic="tada")
    queueconsumer.start()

    commands = {}

    queueconsumer = CommandConsumer(commands, q, stop_event, topic="tada")
    queueconsumer.start()
