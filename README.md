
Todo:
    Import Kafka, create topic, inject messages into topic

    Setup docker:
        app python-alpine
        (?) db mysql: db mount
        kafka kafka mount

    python consumer - create statistical representations or the text
    python bot - would get statistical data from kafka and chat
        + direct messages and direct @'s
        + @'s us and says "bot"

Project:

Connect as a client to any twitch channel (can connect to multiple chats)
    python talis.py <channel>
    python talis.py summit1g

talis.py will read incoming chat messages
    Pipe the message to Kafka topic "chat_messages"

Docker:
    app
    kafka/zookeeper
    mysql

Other codebases:
    consumers/word_count.py
    consumers/word_distribution.py
    ..

# IRC Client Spec
# https://modern.ircdocs.horse/
# https://modern.ircdocs.horse/#connection-registration


Main Website APP

    producer
        push a "event" UserRegister {'username'}

RegisterService
    connects kafka and llistens for "userRegister"
    pipe out EmailUser {}

EmailService
    listen for "Email" {}

twitch chat messages

connects to kafka on message event
    create a new topic
