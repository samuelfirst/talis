import pytest
import json

from talis.formatter import Formatter
from talis.formatter import JsonFormatter

valid_data = [
    ({}, "{}"),
    ([], "[]"),
    (dict(test=1, test2=2), '{"test": 1, "test2": 2}'),
    (list("test"), '["t", "e", "s", "t"]'),
    ({'channel': "talis", 'message': "test message"},
     "{\"channel\": \"talis\", \"message\": \"test message\"}")
]

invalid_types = [
    ("string", TypeError),
    (object, TypeError),
    (b"", TypeError)
]


def test_json_formatter_type():
    assert issubclass(JsonFormatter, Formatter) is True, (
        'JsonFormatter '
        'must be of instance `Formatter`'
    )


@pytest.mark.parametrize('invalid,expected', invalid_types)
def test_json_formatter_invalid_type(invalid, expected):
    with pytest.raises(expected) as e_info:
        JsonFormatter().format(invalid)


@pytest.mark.parametrize('valid,expected', valid_data)
def test_json_formatter_valid_type(valid, expected):
    assert JsonFormatter().format(valid) == expected
