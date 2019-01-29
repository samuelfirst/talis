import configargparse
import os

config_parse = configargparse.ArgParser(default_config_files=['.env', 'local.env'], config_file_parser_class=configargparse.DefaultConfigFileParser)
config_parse.add('-c', '--config', required=False, is_config_file=True, help='Config File Path (*.env)')
config_parse.add('-v', help='verbose', action='store_true')
config_parse.add('-tc', '--TWITCH_CHANNEL', env_var='TWITCH_CHANNEL', help="The Twitch Chat Channel")
config_parse.add('-kh', '--KAFKA_BOOTSTRAP_HOST', env_var='KAFKA_BOOTSTRAP_HOST', help='The kafka host (bootstrap_server)')
config_parse.add('-n', '--TWITCH_NICK', env_var='TWITCH_NICK', help='The Twitch Nickname/Username for the Bot')
config_parse.add('-oa', '--TWITCH_NICK_OAUTH_FILE', env_var='TWITCH_NICK_OAUTH_FILE', help='The Twitch Nick oAuth File')


class AppConfig(object):

    def __init__(self, config_parse):
        self.config_parse = config_parse
        self._calculate_others_init()

    def _parse(self):
        self.config = self.config_parse.parse_known_args()

    def _calculate_others_init(self):
        self._parse()

    def _calculate_oauth_token(self):
        oauth_file = self.get('TWITCH_NICK_OAUTH_FILE')
        if oauth_file is not None:
            oauth_file_isfile = os.path.isfile(oauth_file)

            if oauth_file_isfile:
                f = open(oauth_file, 'r')
                oauth_token = f.readline().rstrip(" \n")
                f.close()
                self.config_parse.add('-tot', '--TWITCH_OAUTH_TOKEN', default=oauth_token)
        self._parse()


    def add_oauth(self):
        self._calculate_oauth_token()

    def get(self, name, default=""):
        # known arguments
        if name in self.config[0]:
            return getattr(self.config[0], name)
        # not known
        else:
            variable = "--{0}".format(name)
            if variable in self.config[1]:
                variable_i = self.config[1].index(variable)
                return self.config[1][variable_i+1]
        return default or None

config = AppConfig(config_parse)
