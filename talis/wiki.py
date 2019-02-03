import threading

from talis import log
from talis.twitch_schema import twitch_schema
from talis.algos import TFIDF
from talis.vendor import Wikipedia
from talis.algos import subject_parser


def wiki(data, question, bot_message_queue):
    wiki.wiki = Wikipedia()
    wiki.algo = TFIDF()
    wiki.response = None

    try:
        subject = subject_parser(question)
        log.info("Found subject {}".format(subject))
        if not subject:
            return

        log.info("Received subject {}".format(subject))
        wiki.algo.set_data(wiki.wiki.get_content(subject))
        log.info("Procsesed subject")

        log.info("Getting Answer")
        wiki.response = wiki.algo.answer(question)
        log.info("Got Answer {}".format(wiki.response))
    except:
        raise

    if wiki.response:
        data_answer = twitch_schema.as_dict(
            data.get('channel'),
            wiki.response
        )
        bot_message_queue.put_nowait(data_answer)
        log.info('Wiki processed')
