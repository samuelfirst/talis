import logging

import pytest

from talis.log import default_handler, log


@pytest.fixture(autouse=True)
def reset_logging(pytestconfig):
    root_handlers = logging.root.handlers[:]
    logging.root.handlers = []
    root_level = logging.root.level

    log = logging.getLogger("talis.app")
    log.handlers = [default_handler]
    log.setLevel(logging.NOTSET)

    logging_plugin = pytestconfig.pluginmanager.unregister(name="logging-plugin")

    yield

    logging.root.handlers[:] = root_handlers
    logging.root.setLevel(root_level)

    log.handlers = [default_handler]
    log.setLevel(logging.NOTSET)

    if logging_plugin:
        pytestconfig.pluginmanager.register(logging_plugin, "logging-plugin")


def test_log():
    assert log.name == "talis.app"
    assert log.level == logging.NOTSET
    assert log.handlers == [default_handler]
