
from python_twitch_irc import TwitchIrc

class Main(TwitchIrc):
    def __init__(self, config : dict):
        self.config = config
        self.channel = self.get_config("channel")
        self.bot_name = self.get_config("bot_name")
        self.max_rate_limit = self.get_config("rate_limit")
        self.oauth = self.get_config("oauth")
        super().__init__(self.bot_name, self.oauth, self.get_config("host"), self.get_config("port"))

    def get_config(self, value):
        if value in self.config:
            return self.config[value]
        else:
            raise ValueError("{0} Shit is not in the config bro".format(value))

    def on_connect(self):
         self.join("#{0}".format(self.channel))

    def on_message(self, timestamp, tags, channel, user, message):
        print("({0}) {1}: {2}".format(channel, user, message))
