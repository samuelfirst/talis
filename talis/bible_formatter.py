import re
from collections import OrderedDict


class BibleFormatter(object):
    def __init__(self):
        pass

    @staticmethod
    def format(data):
        if not isinstance(data, str):
            raise TypeError("Data needs to be of type `str`")

        return BibleFormatter._format(data)

    @staticmethod
    def _format(data):
        """
        replace \n\n \n - solved
        replace {0-9}:{0-9} with ''
        replace : with .\n
        """
        if not data:
            return

        data = re.sub(r"([0-9].?):([0-9].?)", "", data)
        data = re.sub(r" +", " ", data)
        data = data.replace(":", ".")
        data = re.sub(r" +", " ", data)
        data = data.strip()
        return data
