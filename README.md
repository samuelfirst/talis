# Talis

Author: Jon Kirkpatrick

**A Microservice NLP (Natural Language Processing) Twitch Bot written in Python 3 that utilizes Docker, Kafka and Zookeeper.**

The general idea of the Bot was the ability to attach and detach "services" to the bot, at will, and dynamically, without destroying, disconnected and restarting the bot. The bot is highly fault-tolerant, in that the attached services have no "connection" or "knowledge" of the bot, and the bot has no knowledge of the services.

The end goal is to generate a bot that can interact and chat like a "real" twitch user using NLP and the ability to attach and detach services on the fly.

### Bot.py

The primary script ran inside of the python docker container (or localhost with the ```-kh localhost:9092```). You need at least kafka and zookeeper containers launched. This producer connects to Twitch's IRC server and joins the specified channel located in your .env file (or the argument passed with ```-tc <channel>```). This producer pipes the chat messages into a Kafka topic assigned in the .env file.

### Service: Spam 

Launching this service attaches to the Kafka Topic "twitch_messages" and processes and calculates unique messages in a N-range bin log of recent messages. It will send a message to "bot_messages" on Kafka with what text message the bot should send to chat. It basically just spams with chat but can be used to trigger other events like the **Service Clip Producer**

### Service: Wiki 

Launching this service will allow chat to send questions to the bot with ```!q <question>```. It will try it's best to parse the subject and return a response. ie. ```!q what is twitter?```

You can view the other scripts in the AI folder.

![test image size](https://i.imgur.com/6jeuloa.png)

### Service: Commands

Launching this service will allow chat to send commands to the bot with ```!<command>```. It will return a static response based on the input. ie. ```!git```. The commands are not dynamic, but will be dynamic in the future.

### Service: Twitch NLP 

Launching this service will have the bot talk in chat. You can pass in any DOC (corpus) file. In this case, the default is a Twitch Corpus. It talks like a twitch user. Use ```--doc-file data/<file>``` to load a specific doc. A bible doc is also provided to speak the word of god (hehe).

### Service: Clip Producer

Launching this service will have the bot create 10 second clips of the channel by pipping the stream data onto your PC (saves as an MP4). It's currently hooks into the spam service to trigger, but is currently being rewritten.

### Scripts: Send Command

Launching this script will allow you to type from the bot itself. Pass ```:join: <channel>``` to force the bot into a channel. It will join my channel and post the link to where it's going. The notification channel be dynamic in the future.

### Scripts: Consumer

Launching these scripts relate to kafka output and testing. Run ```consumer_test.py``` to test a kafka topic for input and ```consumer_to_file.py``` to save a kafka topic for further DOC processing.

### To run:

1. Get an oAuth token for your bot/user using the twitch password generator
2. place the entire oauth:token text in the .oauth file (ignored with .gitignore)
3. update the channel name in the .env folder or use the ```-tc <channel>``` argument
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

The topic is option and will default to env ```KAFKA_TOPIC```

```
python ai/consumer_test.py -kh localhost:9092 --topic twitch_messages
```

### Tests:

```
./run-tests
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
