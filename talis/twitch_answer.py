import threading
import random

from talis import config
from talis import log
from talis.twitch_schema import twitch_schema
from talis.algos import TFIDF
from cachetools import cached, TTLCache

def twitch_answer(data, question, bot_message_queue):
    twitch_answer.response = None
    twitch_answer.algo = TFIDF()
    twitch_answer.algo.set_punc_remove(False)
    twitch_answer.at_threshold = 0.20

    # dont think will work..
    @cached(cache=TTLCache(maxsize=2000000, ttl=600))
    def load_doc():
        log.info("Loading DOC File.")
        file = open('data/twitch_doc.txt', 'r')
        twitch_answer.algo.set_doc(file.read().split("\n"))
        file.close()


    load_doc()
    log.info("DOC Loaded.")

    try:
        response = twitch_answer.algo.answer(question)
        log.info("Found Response {}".format(response))
    except:
        raise

    if response is not None:
        r = random.randint(1, 10) / 10
        if r <= twitch_answer.at_threshold:
            response = ('@' + data.get('channel') +
              " " + response)

        log.info("New Response {}".format(response))
        data_to_send = twitch_schema.as_dict(
            data.get('channel'),
            response
        )
        bot_message_queue.put_nowait(data_to_send)
