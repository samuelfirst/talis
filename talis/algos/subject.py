import nltk

from talis import log


def subject_parser(sentence):
    '''
        Trys to nastily parse a subject
        from a sentence
    '''
    nltk.download('averaged_perceptron_tagger')
    is_noun = lambda pos: pos[:2] == 'NN'
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
