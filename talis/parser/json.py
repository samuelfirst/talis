import json

from talis.parser import Parser

class JsonParser(Parser):

    @staticmethod
    def parse(data):
        if not isinstance(data, (str, bytes)):
            raise TypeError("Data needs to be of type `str` or `bytes` to parse")

        return getattr(JsonParser, '_from_%s' % type(data).__name__)(data)

    @classmethod
    def _parse(cls, data):
        return json.loads(data)

    @classmethod
    def _from_bytes(cls, data):
        return cls._parse(data.decode('utf-8'))

    @classmethod
    def _from_str(cls, data):
        return cls._parse(data)
