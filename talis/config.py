
from dotenv import load_dotenv
from pathlib import Path

import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

oauth_exists = os.path.isfile(os.getenv("OAUTH_TOKEN_FILE"))

if oauth_exists:
    f = open(os.getenv("OAUTH_TOKEN_FILE"), 'r')
    os.environ["OAUTH_TOKEN"] = f.readline().rstrip(" \n")
    f.close()
