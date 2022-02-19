from typing import NamedTuple


class TwitchSchema(NamedTuple):
    channel: str
    message: str

    @classmethod
    def as_dict(cls, channel, message):
        return cls(channel, message)._asdict()
