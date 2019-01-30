import pytest
import json

from talis.parser import Parser
from talis.parser import JsonParser

invalid_tpes = [
    ({}, TypeError),
    ([], TypeError),
    (dict(test=1, test2=2), TypeError),
    (list("test"), TypeError),
    ({'channel': "talis", 'message': "test message"},
     TypeError)
]

valid_data = [
    ("{\"test\": \"string\"}", {'test': 'string'}),
    (b"{}", {}),
    ("{\"channel\": \"talis\", \"message\": \"test message\"}",
     {'channel': "talis", 'message': "test message"})
]

def test_json_parseter_type():
    assert True == issubclass(JsonParser, Parser), 'JsonParser must be of instance `Parser`'

@pytest.mark.parametrize("invalid, expected", invalid_tpes)
def test_json_parseter_invalid_type(invalid, expected):
    with pytest.raises(expected) as e_info:
        JsonParser().parse(invalid)

@pytest.mark.parametrize("valid, expected", valid_data)
def test_json_parseter_valid_type(valid, expected):
    assert JsonParser().parse(valid) == expected
