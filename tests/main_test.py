from . import *

class MainTest(MainTestCase):

    def test_get_config(self):
        assert self.main.get_config("host") == "host_name"
        assert self.main.get_config("port") == 1337
        assert self.main.get_config("bot_name") == 'imabot'
        assert self.main.get_config("oauth") == 'oauth:132423'
        assert self.main.get_config("log_level") == 10
