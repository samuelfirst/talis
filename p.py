
from talis.kafka import TwitchSchema
import json

data = TwitchSchema('jonthomask', 'testing')

print(data)
print(json.dumps(data._asdict()))
