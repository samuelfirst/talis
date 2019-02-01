import pytest

from unittest import mock
from unittest.mock import patch

from talis.kafka.consumer import KafkaConsumerFactory
from talis.kafka.consumer import TalisConsumer

from kafka import KafkaConsumer


class TestConsumerFactory(object):

    @patch.object(KafkaConsumerFactory, '__init__', return_value=None)
    @patch.object(KafkaConsumerFactory, 'create', return_value="called")
    def test_create(self, mocked_kafka_consumer, mocked_init):
        kafka_consumer_factory = KafkaConsumerFactory.create(
            'topic'
        )
        mocked_init.assert_not_called()
        assert kafka_consumer_factory == "called"


class TestConsumer(object):

    @patch.object(KafkaConsumerFactory, 'create', return_value="called")
    def test_init(self, mocked_kafka_consumer_factory):
        talis_consumer = TalisConsumer(topic='talis')
        assert talis_consumer.topic == 'talis'
        assert talis_consumer.consumer == 'called'
