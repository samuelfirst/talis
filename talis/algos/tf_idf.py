import nltk
import numpy as np
import random
import string
import spacy
import re
import logging

from spacy.symbols import nsubj, VERB, PROPN, NOUN

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from talis import log

log.setLevel(logging.INFO)

class TFIDF(object):

    def __init__(self):
        nltk.download('punkt')
        nltk.download('wordnet')
        self.nlp = spacy.load('en')
        self.raw_data = ""
        self.subject = None
        self.sent_tokens = []
        self.word_tokens = []
        self.lemmer = nltk.stem.WordNetLemmatizer()
        self.remove_punct_dict = dict(
            (ord(punct), None) for punct in string.punctuation
        )
        self.ai_response = None

    def set_data(self, raw_data):
        self.raw_data = raw_data
        self.sent_tokens = nltk.sent_tokenize(self.raw_data)
        self.word_tokens = nltk.word_tokenize(self.raw_data)

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(
            nltk.word_tokenize(text.translate(self.remove_punct_dict))
        )

    def set_subject(self, question):
        doc = self.nlp(question)

        proper_nouns = []
        if ("is" or "was") in question:
            flag = False
            for token in doc:
                token_str = token.string.strip()
                if token_str == "is" or token_str == "was":
                    flag = not flag
                    continue
                if (token.pos == VERB or token.pos == NOUN) and flag:
                    proper_nouns.append(token_str)

        if not len(proper_nouns):
            for token in doc:
                if (token.pos == PROPN):
                    proper_nouns.append(token.string)

        if len(proper_nouns):
            log.info("Setting Subject: {}".format(" ".join(proper_nouns)))
            self.subject = " ".join(proper_nouns)
        else:
            self.subject = None

    def answer(self, input_text):
        if self.subject is None:
            self.ai_response = "I'm sorry, I can't find the subject"
            return self.ai_response
        self.sent_tokens.append(input_text.lower())
        TfidfVec = TfidfVectorizer(
            tokenizer=self.LemNormalize,
            stop_words='english'
        )
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf == 0):
            self.ai_response = "I'm sorry, I don't know the answer."
        else:
            if (self.sent_tokens[idx] == ""):
                self.ai_response = "I'm sorry, I can't find an answer on that page."
            else:
                self.ai_response = self.sent_tokens[idx]
        self.sent_tokens.remove(input_text.lower())
        return self.ai_response
