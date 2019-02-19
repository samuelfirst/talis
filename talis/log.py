import logging

default_handler = logging.StreamHandler()
default_handler.setFormatter(logging.Formatter(
    '%(levelname)s\t%(module)s:\t %(message)s'
))

log = logging.getLogger("talis.app")
log.addHandler(default_handler)
