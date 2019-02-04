# Talis

***Author: Jon Kirkpatrick***

A Microservice NLP (Natural Language Processing) Twitch Bot written in Python 3 that utilizes Docker, Kafka and Zookeeper.

The general idea of the Bot was the ability to attach and detach "services" to the bot, at will, and dynamically, without destroying, disconnected and restarting the bot. The bot is highly fault-tolerant, in that the attached services have no "connection" or "knowledge" of the bot, and the bot has no knowledge of the services.

The end goal is to generate a bot that can interact and chat like a "real" twitch user using NLP and the ability to attach and detach services on the fly.

This is the next general step into creating a hive mind AI that can attach and disconnect micro-ai services at will.

***Bot.py*** is the primary script ran inside of the python docker container. This producer connects to Twitch's IRC server and joins the specified channel located in your .env file. This producer pipes the chat messages into a Kafka topic assigned in the .env file.

***AI/spam*** is an example service that attaches to the Kafka Topic "twitch_messages" and processes and calculates unique messages in a N-range bin log of recent messages. It will send a message to "bot_messages" on Kafka with what text message the bot should send to chat.

You can view the other scripts in the AI folder.

![test image size](https://i.imgur.com/6jeuloa.png)

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
```

### With docker:

```docker-compose up --build -d```

### Without docker:

You *will* need to launch the kafka + zookeeper containers in order for the scripts to work. Once you have them up you can run the bot like so:

```python bot.py -tc <channel> -kh localhost:9092```


***To see if the bot worked (when using Docker for bot):***

```
docker logs -f talis_app
```

You should see messages piping out to your console.

***To test if kafka is receiving the messages:***
```
python ai/consumer_test.py -kh localhost:9092
```

## Todo:
- [ ] private message response and @response integration
- [ ] The messages AI/spam.py messages sent to the bot is user input and not escaped properly. Create an interface to filter out piped messages.
- [x] Build Kafka Schema for data construction
- [ ] utf-8 all over the place, fix
- [x] Travis
- [x] Threads: NLP revealed thread issue with multiqueries

## Feature List:
- [x] The ability to send the bot to any channel
- [x] Teach it the bible for fun
