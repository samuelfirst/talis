'''
Use this script to create a twitch doc
for nlp processing
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis import BibleFormatter


def open_doc(name, code):
    with open(name, code) as file:
        for line in file:
            yield line


if __name__ == "__main__":

    bible_formatter = BibleFormatter()

    with open('data/bible_doc.txt', 'w') as doc:
        for line in open_doc('data/bible.txt', 'r'):
            formatted = bible_formatter.format(line)
            if len(formatted):
                doc.write(formatted + "\n")
