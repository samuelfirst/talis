"""
user this script to send a bot command
"""
import json
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.realpath(__name__)))

from kafka import KafkaConsumer, KafkaProducer

from talis import config, log, TwitchSchema

if __name__ == "__main__":

    kafka_producer = KafkaProducer(
        bootstrap_servers=config.get("KAFKA_BOOTSTRAP_HOST"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    try:
        while True:
            command = input("What Message?\n")

            central_control = re.findall(r"^(:join: )(.+)", command)
            print(central_control)
            if central_control and len(central_control[0]) == 2:
                print("found parsed ADMIN command")
                central_control = central_control[0]
                command = central_control[0]
                channel = central_control[1]
                kafka_topic = "central_control"
                data = TwitchSchema.as_dict(config.get("TWITCH_CHANNEL"), channel)
            else:
                kafka_topic = config.get("KAFKA_BOT_MESSAGE_TOPIC")
                data = TwitchSchema.as_dict(config.get("TWITCH_CHANNEL"), command)

            kafka_producer.send(kafka_topic, data)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        raise
