'''
This script will attach and listen for
bot messages (temporary location for testing) and will
generate a 10 second clip of the channel where "hype" occurred
'''
import queue
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from talis import config
from talis import log

if __name__ == "__main__":
    '''
        This needs to be redo so it can queue
        off the proper kafka topic
    '''
    pass
