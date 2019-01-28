# Talis

***Author: Jon Kirkpatrick***

A Microserviced NLP (Natural Language Processing) Twitch Bot written in Python 3 that utilizes Docker, Kafka and Zookeeper.

The general idea of the Bot was the ability to attach and detach "services" to the bot, at will, and dynamically, without destroying, disconnected and restarting the bot. The bot is highly fault-tolerant, in that the attached services have no "connection" or "knowledge" of the bot, and the bot has no knowledge of the services.

The end goal is to generate a bot that can interact and chat like a "real" twitch user using NLP and the ability to attach and detach services on the fly.

This is the next general step into creating a hive mind AI that can attach and disconnect micro-ai services at will.

***Twitch Message Producer*** is the primary script ran inside of the python docker container. This producer connects to Twitch's IRC server and joins the specified channel located in your .env file. This producer pipes the chat messages into a Kafka topic assigned in the .env file.

***Bot*** is the bot that interacts with chat. This bot starts off with no attachments and listens on the topic "bot_messages". It awaits commands from other services. The bot does have a temporary rule based consumer embedded.

***AI/spam*** is an example service that attaches to the Kafka Topic "twitch_messages" and processes and calculates unique messages in a N-range bin log of recent messages. It will send a message to "bot_messages" on Kafka with what text message the bot should send to chat.


### To run:

1. Get an oAuth token for your bot/user using the twitch password generator
2. place the entire oauth:token text in the .oauth file
3. update the channel name in the .env folder
4. Run these commands:

```
pip install virtualenv
python -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
docker-compose up --build -d
```

***To see if the bot worked:***

```
docker logs -f talis_app
```

You should see messages piping out to your console.

***To test if kafka is receiving the messages:***
```
python ai/consumer_test.py
```

## Todo:
- [ ] private message response and @responses
- [ ] filter out messages from the bot itself
- [ ] ai/consumer_to_file.py  --> data/debug_*.txt (compress please)
- [ ] The messages AI/spam.py sends to the bot is user input and not escaped properly. Create an interface to filter out piped messages
