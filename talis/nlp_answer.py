import threading
import random

from talis import config
from talis import log
from talis.twitch_schema import twitch_schema
from talis.algos import TFIDF
from cachetools import cached, TTLCache


def nlp_answer(data, question, bot_message_queue, doc_file):
    nlp_answer.response = None
    nlp_answer.algo = TFIDF()
    nlp_answer.at_threshold = 0.10

    log.info("Calculating Response...")

    # dont think will work..
    # @cached(cache=TTLCache(maxsize=2000000, ttl=600))
    def load_doc(file_name):
        file = open(file_name, 'r')
        nlp_answer.algo.set_doc(file.read().split("\n"))
        file.close()

    load_doc(doc_file)

    try:
        response = nlp_answer.algo.answer(question)
    except:
        raise

    if response is not None:
        # TODO: need a way to get global config
        # username = None
        # if data.get('username'):
        #     username = data.get('username')
        # else:
        #     r = random.randint(1, 100) / 100
        #     if r <= nlp_answer.at_threshold:
        #         username = config.get('TWITCH_CHANNEL')
        #
        # if username:
        #     response = (
        #         '@' + username + " " + response
        #     )

        log.info("New Response: {}".format(response))
        data_to_send = twitch_schema.as_dict(
            data.get('channel'),
            response
        )
        bot_message_queue.put_nowait(data_to_send)
    else:
        log.info("No Response found.")
