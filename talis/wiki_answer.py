import threading

from talis import log
from talis.algos import TFIDF, subject_parser
from talis.twitch_schema import TwitchSchema
from talis.vendor import Wikipedia


def wiki_answer(data, question, bot_message_queue):
    wiki_answer.wiki_answer = Wikipedia()
    wiki_answer.algo = TFIDF()
    wiki_answer.response = None

    try:
        subject = subject_parser(question)
        log.info("Found subject {}".format(subject))
        if not subject:
            return

        log.info("Received subject {}".format(subject))
        wiki_answer.algo.set_data(wiki_answer.wiki_answer.get_content(subject))
        log.info("Processed subject")

        log.info("Getting Answer")
        wiki_answer.response = wiki_answer.algo.answer(question)
        log.info("Got Answer {}".format(wiki_answer.response))
    except:
        raise

    if wiki_answer.response:
        data_answer = TwitchSchema.as_dict(data.get("channel"), wiki_answer.response)
        bot_message_queue.put_nowait(data_answer)
        log.info("Wiki processed")
    else:
        log.info("No response {}".format(wiki_answer.response))
