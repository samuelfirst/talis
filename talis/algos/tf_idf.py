import logging
import string

import nltk

from talis import log

log.setLevel(logging.INFO)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDF(object):
    def __init__(self):
        self.data = ""
        self.sent_tokens = []
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.response = None
        self.remove_punct_dict = dict(
            (ord(punct), None) for punct in string.punctuation
        )

    # doc is already in sentence formart
    def set_doc(self, doc):
        self.data = doc
        self.sent_tokens = self.data

    # only used if the doc needs sentences
    # ..parsed
    def set_data(self, data):
        self.data = data
        if self.data:
            self.sent_tokens = nltk.sent_tokenize(self.data)

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(
            nltk.word_tokenize(text.translate(self.remove_punct_dict))
        )

    def answer(self, input_text):
        self.sent_tokens.append(input_text.lower())
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words="english")
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            self.response = None
        else:
            if self.sent_tokens[idx] == "":
                self.response = None
            else:
                self.response = self.sent_tokens[idx]
        self.sent_tokens.remove(input_text.lower())
        return self.response
