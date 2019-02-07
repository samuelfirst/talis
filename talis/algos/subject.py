
from talis import log

try:
    import nltk
except:
    nltk = None
    log.info("NLTK is not installed. Are we testing?")


def is_noun(pos):
    return pos[:2] == 'NN'


def subject_parser(sentence):
    '''
        Trys to nastily parse a subject
        from a sentence
    '''
    # todo: add to docker base image
    nltk.download('averaged_perceptron_tagger')
    doc = nltk.word_tokenize(sentence)
    subject = None
    nouns = []

    if "is" in sentence or "was" in sentence:
        flag = False
        for word, pos in nltk.pos_tag(doc):
            print(word, pos)
            if (word == "is" or word == "was") and not flag:
                flag = not flag
                continue
            if pos != "." and flag:
                nouns.append(word)

    if not len(nouns):
        nouns = [word for (word, pos) in nltk.pos_tag(doc) if is_noun(pos)]

    if len(nouns):
        log.debug("Setting Subject: {}".format(" ".join(nouns)))
        subject = " ".join(nouns)
    return subject
