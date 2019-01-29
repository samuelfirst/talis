import json

from talis.formatter import Formatter

class JsonFormatter(Formatter):

    @staticmethod
    def format(data):
        if not isinstance(data, (dict, list)):
            raise TypeError("Data needs to be of type `dict` or `list` to format")

        return getattr(JsonFormatter, '_from_%s' % type(data).__name__)(data)

    @classmethod
    def _format(cls, data):
        return json.dumps(data)

    @classmethod
    def _from_dict(cls, data):
        return cls._format(data)

    @classmethod
    def _from_list(cls, data):
        return cls._format(data)
