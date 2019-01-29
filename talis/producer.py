from kafka import KafkaProducer

from talis.processor import DataProcessor

class TalisProducer(object):

    def __init__(self, data_processor, *args, **kwargs):
        if not isinstance(data_processor, DataProcessor):
            raise TypeError("The data_processor argument must be a valid DataProcessor object.")

        self.sent = 0
        self.data_processor = data_processor
        self.topic = kwargs['topic']
        del kwargs['topic']
        try:
            self.producer = KafkaProducer(*args, **kwargs)
        except:
            raise
