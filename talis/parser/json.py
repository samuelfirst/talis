import json

from talis.parser import Parser

class JsonParser(Parser):

    def parse(self, data):
        return json.dumps(data)
