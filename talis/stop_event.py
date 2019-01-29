from threading import Event

class TalisStopEvent(object):

    def __init__(self, stop_event):
        if not isinstance(stop_event, Event):
            raise BasicException("Stop Event needs to be a threading.Event")
        self.stop_event = stop_event
