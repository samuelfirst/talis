import spacy

from talis import log

from spacy.symbols import nsubj, VERB, PROPN, NOUN, amod, attr, ADJ


def subject_parser(sentence):
    '''
        Trys to nastily parse a subject
        from a sentence
    '''
    nlp = spacy.load('en')
    doc = nlp(sentence)
    subject = None

    proper_nouns = []
    for token in doc:
        if (token.dep == PROPN or token.dep == NOUN):
            proper_nouns.append(token.string)

    if not len(proper_nouns):
        if ("is" or "was") in sentence:
            flag = False
            for token in doc:
                token_str = token.string.strip()
                if token_str == "is" or token_str == "was":
                    flag = not flag
                    continue
                if (
                    token.pos == VERB or
                    token.pos == NOUN or
                    token.pos == PROPN or
                    token.pos == ADJ
                ) and flag:
                    print("added {}".format(token_str))
                    proper_nouns.append(token_str)

    if "who" in proper_nouns:
        proper_nouns.remove("who")

    if len(proper_nouns):
        log.info("Setting Subject: {}".format(" ".join(proper_nouns)))
        subject = " ".join(proper_nouns)
    return subject
