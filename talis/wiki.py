import threading

from talis import log
from talis import twitch_schema
from talis.algos import TFIDF
from talis.vendor import Wikipedia
from talis.algos import subject_parser


def wiki(data, question, bot_message_queue):
    wiki_consumer.wiki = Wikipedia()
    wiki_consumer.algo = TFIDF()
    wiki_consumer.response = None

    try:
        subject = subject_parser(question)
        log.info("Found subject {}".format(subject))
        if not subject:
            return

        log.info("Received subject {}".format(subject))
        wiki_consumer.algo.set_data(wiki_consumer.wiki.get_content(subject))
        log.info("Procsesed subject")

        log.info("Getting Answer")
        wiki_consumer.response = wiki_consumer.algo.answer(question)
        log.info("Got Answer {}".format(wiki_consumer.response))
    except:
        raise

    if wiki_consumer.response:
        data_answer = twitch_schema.as_dict(
            data.get('channel'),
            wiki_consumer.response
        )
        bot_message_queue.put_nowait(data_answer)
        log.info('Wiki processed')
