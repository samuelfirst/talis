import json

from talis.parser import Parser


class JsonParser(Parser):

    def parse(self, data):
        if not isinstance(data, (str, bytes)):
            raise TypeError(
                "Data needs to be of type `str` "
                "or `bytes` to parse"
            )

        if type(data).__name__ == 'bytes':
            return self._parse(data.decode('utf-8'))

        return self._parse(data)

    def _parse(self, data):
        return json.loads(data)
