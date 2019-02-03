# import threading
# import time
# import random
# import re
#
# from talis import config
# from talis import log
#
# from talis.kafka.queue_consumer import QueueConsumer
# from talis.kafka.twitch_schema import TwitchKafkaSchema
# from talis.formatter import TwitchFormatter
#
# from talis.algos import TFIDF
#
#
# class TwitchNLP(QueueConsumer, threading.Thread):
#     '''
#         TODO: Clean up this class. It was for getting
#         out a quick demo of wikipedia interaction.
#     '''
#     def __init__(self, queue, stop_event,
#                  data_processor, *args, **kwargs):
#         QueueConsumer.__init__(self, queue, stop_event, *args, **kwargs)
#         threading.Thread.__init__(self)
#         self.set_data_processor(data_processor)
#         self.twitch_formatter = TwitchFormatter()
#         self.algo = TFIDF()
#         self.seen_messages = 0
#         self.start_time = 0
#         self.messages_sec = 0
#         self.chatter_level = 10
#         self.last_chatter = 0
#         self.accuracy = 3
#         self.message_bin = []
#
#     def do_response(self, data, input_text):
#         response = None
#         try:
#             response = self.algo.answer(input_text)
#             print(response)
#         except:
#             raise
#
#         if response is not None:
#             r = random.randint(1, 10)
#
#             if r <= 2:
#                 response = '@' + config.get('TWITCH_CHANNEL') +
#                   " " + response
#
#             data_to_send = TwitchKafkaSchema.as_dict(
#                 data.get('channel'),
#                 response
#             )
#             self.queue.put_nowait(
#                 bytes(
#                     self.data_processor.format(data_to_send),
#                     'utf-8'
#                 )
#             )
#             print("Sent to bot")
#             self.last_chatter = time.time()
#
#     def process_message(self, msg):
#         data = self.data_processor.parse(msg)
#         message = data.get('message')
#         msg = self.twitch_formatter.format(message)
#         if not len(msg):
#             return
#
#         at_ = re.match(r'\@(?P<username>(.+? ))', message)
#         if at_:
#             at_ = at_["username"].strip()
#
#         now = time.time()
#         self.processed += 1
#         self.message_bin.append(msg)
#         self.messages_sec = self.processed / (now - self.start_time)
#
#         print("{:.02f}".format(self.messages_sec))
#
#         if (
#             (len(self.message_bin) >= self.chatter_level) and
#             ((now - self.last_chatter) > self.chatter_level)
#         ):
#             input_text = self.message_bin[self.chatter_level - self.accuracy]
#             self.message_bin = []
#
#             print("TWITCH CHATTER: {}".format(input_text))
#             self.do_response(data, input_text)
#         elif at_ == config.get('TWITCH_NICK'):
#             input_text = message.strip('@' + config.get('TWITCH_NICK'))
#             self.message_bin = []
#
#             print("TWITCH CHATTER @: {}".format(input_text))
#             self.do_response(data, input_text)
#
#     def run(self):
#         while not self.stop_event.is_set():
#             for msg in self.consumer:
#                 self.process_message(msg.value)
#             if self.stop_event.is_set():
#                 break
