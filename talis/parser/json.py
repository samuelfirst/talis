import json

from talis.parser import Parser

class JsonParser(Parser):

    def parse(self, data):
        data_type = type(data).__name__

        try:
            parsed_data = getattr(JsonParser, 'from_%s' % data_type)(data)
        except:
            raise
        return parsed_data

    @classmethod
    def _parse(cls, data):
        return json.loads(data)

    @classmethod
    def from_bytes(cls, data):
        return cls._parse(data.decode('utf-8'))

    @classmethod
    def from_str(cls, data):
        return cls._parse(data)
