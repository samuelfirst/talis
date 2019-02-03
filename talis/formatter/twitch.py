import re

from collections import OrderedDict
from talis.formatter import Formatter


class TwitchFormatter(Formatter):

    def format(self, data):
        if not isinstance(data, str):
            raise TypeError(
                "Data needs to be of type `str`"
            )

        return self._format(data)

    def _format(self, data):
        if len(data) == 1:
            return ""

        data = re.sub(r'^!(.+?)', '', data)
        data = re.sub(r'\@(.+?)', '', data)
        data = re.sub(r' +', ' ', data)

        if len(list(data)) == 0:
            "".join(OrderedDict.fromkeys(data))

        data = " ".join(list(OrderedDict.fromkeys(data.split(" "))))

        data = re.sub(r'https?:\/\/.*[\r\n]*', '', data)
        data = re.sub(r' +', ' ', data)
        data = data.strip()
        return data

        # for each message
        #     remove .{1} <-- single character
        #     remove !() <- commands
        #     remove @() <-- user messages
        #
        #     remove links
        #     remove {0} {0} duplicate posts/spam
        #
        #     remove duplicate messages
        #     add . to end of each line?
