import json

from talis.formatter import Formatter

class JsonFormatter(Formatter):

    def format(self, data):
        if not isinstance(data, (dict, list)):
            raise TypeError("Data needs to be of type `dict` or `list` to format")

        return self._format(data)

    def _format(self, data):
        return json.dumps(data)
