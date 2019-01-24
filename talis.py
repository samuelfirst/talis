import sys, logging, os

from talis import Main

HOST_NAME = "irc.chat.twitch.tv"
PORT = 6667
BOT_NAME = "talis_jtk"
OAUTH_TOKEN_FILE = '.oauth'

# The IRC imposes a 20 second message/command limit
# within a 30 second window
RATE_LIMIT = 20
RATE_LIMIT_TIME = 30000

# DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.DEBUG

oauth_exists = os.path.isfile(OAUTH_TOKEN_FILE)

config = {
    'host' : HOST_NAME,
    'port' : PORT,
    'bot_name' : BOT_NAME,
    'log_level' : LOG_LEVEL,
    'rate_limit' : RATE_LIMIT,
    'rate_limit_time': RATE_LIMIT_TIME
}

_l = logging.getLogger("talis_app")
ch = logging.StreamHandler()

formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)

_l.setLevel(config['log_level'])
ch.setLevel(config['log_level'])

_l.addHandler(ch)

if not oauth_exists:
    _l.critical("{} token file does not exist.".format(OAUTH_TOKEN_FILE))
    exit()

f = open(OAUTH_TOKEN_FILE, 'r')
OAUTH_TOKEN = f.readline().rstrip(" \n")
f.close()

config["oauth"] = OAUTH_TOKEN.lstrip("oauth:")

if __name__ == "__main__":
    _l.info("=== Bot Started ===")
    _l.info("LOG LEVEL: {}".format(config['log_level']))

    (channel,) = sys.argv[1:]
    config['channel'] = channel

    client = Main(config=config).start()
    client.handle_forever()
