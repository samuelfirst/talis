import json

from talis.formatter import Formatter

class JsonFormatter(Formatter):

    def format(self, data):
        data_type = type(data).__name__
        try:
            formatted_data = getattr(JsonFormatter, 'from_%s' % data_type)(data)
        except:
            raise
        return formatted_data

    @classmethod
    def _format(cls, data):
        return json.dumps(data)

    @classmethod
    def from_dict(cls, data):
        return cls._format(data)
