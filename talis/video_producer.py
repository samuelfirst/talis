import threading

import os

from .queue import TalisQueue

class VideoProducer(threading.Thread, TalisQueue):

    def __init__(self, queue, *args, **kwargs):
        threading.Thread.__init__(self)
        TalisQueue.__init__(self, queue)

    # ENTRY POINT FOR THREAD
    def run(self):
        while True:
            try:
                # BLOCKING and THREAD LOCKING
                data = self.queue.get()
            except:
                break
            try:
                channel = data.get('channel')
                print('getting clip of {}'.format(channel))
                os.system("cd ~/sites/talis && source env/bin/activate && nohup python ~/sites/talis/subscripts/record_video.py https://www.twitch.tv/{0} {1} & disown".format(channel, channel))
            except:
                pass
            self.queue.task_done()
