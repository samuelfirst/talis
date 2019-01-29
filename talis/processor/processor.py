from talis.parser import Parser
from talis.formatter import Formatter

class DataProcessor(object):

    def __init__(self, parser, formatter):
        if not isinstance(parser, Parser):
            raise TypeError("parser must be a valid `Parser`")

        if not isinstance(formatter, Formatter):
            raise TypeError("formatter must be a valid `Formatter`")

        self.parser = parser
        self.formatter = formatter

    def parse(self, data):
        return self.parser.parse(data)

    def format(self, data):
        return self.formatter.format(data)
