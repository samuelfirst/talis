

def push_queue(kafka_consumer, talis_queue, stop_event):
    while not stop_event.is_set():
        for msg in kafka_consumer:
            talis_queue.put_nowait(msg.value)


def dequeue(kafka_producer, topic, talis_queue):
    while True:
        data = talis_queue.get()
        kafka_producer.send(topic, data)
        talis_queue.task_done()
