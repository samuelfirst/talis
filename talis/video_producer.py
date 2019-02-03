import threading
import os

from talis import log


# class VideoProducer(threading.Thread):
#
#     def __init__(self, queue, *args, **kwargs):
#         threading.Thread.__init__(self)
#         self.queue = queue
#
#     def run(self):
#         while True:
#             try:
#                 data = self.queue.get()
#             except:
#                 break
#             try:
#                 channel = data.get('channel')
#                 log.info('getting clip of {}'.format(channel))
#                 os.system(
#                     "cd ~/sites/talis && "
#                     "source env/bin/activate && "
#                     "nohup python scripts/record_clip.py "
#                     "https://www.twitch.tv/{0} {1} & disown"
#                     .format(channel, channel)
#                 )
#             except:
#                 pass
#             self.queue.task_done()
