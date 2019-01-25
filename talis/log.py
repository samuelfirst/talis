import logging
import os

from .config import *

log = logging.getLogger("talis_app")
ch = logging.StreamHandler()

formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.setLevel(int(os.getenv("LOG_LEVEL")))
ch.setLevel(int(os.getenv("LOG_LEVEL")))

log.addHandler(ch)
