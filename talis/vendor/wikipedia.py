import wikipedia
import re

class Wikipedia(object):

    def __init__(self):
        pass

    def get_content(self, topic):
        searched = wikipedia.search(topic)
        raw_data = wikipedia.page(searched[0]).content
        return raw_data

    def search(self, topic):
        return wikipedia.search(topic)
