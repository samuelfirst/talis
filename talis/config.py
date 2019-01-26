
from dotenv import load_dotenv
from pathlib import Path

import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

bot_oauth_file = os.path.isfile(os.getenv("TWITCH_BOT_OAUTH_FILE"))
consumer_oauth_file = os.path.isfile(os.getenv("TWTICH_CONSUMER_NICK_OAUTH_FILE"))

if bot_oauth_file:
    f = open(os.getenv("TWITCH_BOT_OAUTH_FILE"), 'r')
    os.environ["TWITCH_BOT_OAUTH_TOKEN"] = f.readline().rstrip(" \n")
    f.close()

if consumer_oauth_file:
    f = open(os.getenv("TWTICH_CONSUMER_NICK_OAUTH_FILE"), 'r')
    os.environ["TWTICH_CONSUMER_NICK_OAUTH_TOKEN"] = f.readline().rstrip(" \n")
    f.close()
