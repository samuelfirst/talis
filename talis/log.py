import logging
import os

from .config import config

log = logging.getLogger("talis_app")
ch = logging.StreamHandler()

formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.setLevel(int(config.get("LOG_LEVEL")))
ch.setLevel(int(config.get("LOG_LEVEL")))

log.addHandler(ch)
