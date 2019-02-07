import re

from collections import OrderedDict


class TwitchFormatter(object):

    def __init__(self):
        pass

    @staticmethod
    def format(data):
        if not isinstance(data, str):
            raise TypeError(
                "Data needs to be of type `str`"
            )

        return TwitchFormatter._format(data)

    @staticmethod
    def _format(data):
        '''
            remove .{1} <-- single character
            remove !() <- commands
            remove @() <-- user messages

            remove links
            remove {0} {0} duplicate posts/spam

            remove duplicate messages
            add . to end of each line?
        '''
        if len(data) == 1:
            return ""

        if "[" in data or "]" in data:
            return ""

        if "ACTION" in data:
            return ""

        if "talis" in data:
            return ""

        data = re.sub(r'^!(.+)', '', data)
        data = re.sub(r'\@(\b.+?\b)', '', data)
        data = re.sub(r' +', ' ', data)

        if len(list(data)) == 0:
            "".join(OrderedDict.fromkeys(data))

        data = " ".join(list(OrderedDict.fromkeys(data.split(" "))))

        data = re.sub(r'https?:\/\/.*[\r\n]*', '', data)
        data = re.sub(r'(summit )', '', data)
        data = re.sub(r'(dan )', '', data)
        data = re.sub(r'(pace )', '', data)
        data = re.sub(r'\'', '', data)
        data = re.sub(r'!(.+)', '', data)
        data = re.sub(r'\!$', '', data)
        data = re.sub(r'\.', '', data)
        data = re.sub(r'\?$', '', data)
        data = re.sub(r'\@', '', data)
        data = re.sub(r' +', ' ', data)
        data = data.strip()
        return data
