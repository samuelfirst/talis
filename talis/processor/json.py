from talis.parser import JsonParser
from talis.formatter import JsonFormatter
from talis.processor import DataProcessor


class JsonProcessor(DataProcessor):
    def __init__(self):
        super().__init__(JsonParser(), JsonFormatter())
