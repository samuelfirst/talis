import pytest

from unittest import mock
from unittest.mock import patch

from talis.kafka.producer import KafkaProducerFactory
from talis.kafka.producer import TalisProducer

from kafka import KafkaProducer


class TestProducerFactory(object):

    @patch.object(KafkaProducerFactory, '__init__', return_value=None)
    @patch.object(KafkaProducerFactory, 'create', return_value="called")
    def test_create(self, mocked_kafka_producer, mocked_init):
        kafka_producer_factory = KafkaProducerFactory.create()
        mocked_init.assert_not_called()
        assert kafka_producer_factory == "called"


class TestProducer(object):

    @patch.object(KafkaProducerFactory, 'create', return_value="called")
    def test_init(self, mocked_kafka_producer_factory):
        talis_producer = TalisProducer()
        assert talis_producer.producer == 'called'
