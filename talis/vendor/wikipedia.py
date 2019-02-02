import wikipedia
import re

from cachetools import cached, TTLCache


class Wikipedia(object):

    def __init__(self):
        self.raw_data = None

    @cached(cache=TTLCache(maxsize=4096, ttl=600))
    def get_content(self, topic):
        searched = self.search(topic)
        self.raw_data = wikipedia.page(searched[0]).content
        return self.normalize()

    def search(self, topic):
        return wikipedia.search(topic)

    def normalize(self):
        self.raw_data = self.raw_data.replace("\n", " ").lower()
        self.raw_data = re.sub(r'(== .*? ==).+', '', self.raw_data, flags=re.I)
        self.raw_data = re.sub(r'(=== .*? ===)', '', self.raw_data)
        self.raw_data = re.sub(r'\(; ', '(', self.raw_data)
        self.raw_data = re.sub(r'\( ', '(', self.raw_data)
        self.raw_data = re.sub(r'\(listen\);', '', self.raw_data)
        self.raw_data = re.sub(r'\[o\.s\.', '', self.raw_data)
        self.raw_data = re.sub(r'\]', '', self.raw_data)
        self.raw_data = re.sub(r' +', ' ', self.raw_data)
        return self.raw_data
