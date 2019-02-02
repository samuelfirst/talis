from typing import NamedTuple


class TwitchKafkaSchema(NamedTuple):
    channel: str
    message: str

    @classmethod
    def as_dict(cls, channel, message):
        return cls(channel, message)._asdict()
