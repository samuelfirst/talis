import abc


class Formatter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def format(data):
        pass
