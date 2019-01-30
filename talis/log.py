import logging

default_handler = logging.StreamHandler()
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))

log = logging.getLogger("talis.app")
log.addHandler(default_handler)
