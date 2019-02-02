'''
user this script to test tf_idf
'''
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log
from talis.vendor import Wikipedia
from talis.algos import TFIDF

if __name__ == "__main__":

    wiki = Wikipedia()
    tf = TFIDF()

    tf.set_data(wiki.get_content("barack obama"))
    print(tf.answer("who is barack obama?"))
