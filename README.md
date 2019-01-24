###
# What I am doing:
###

Project:

Connect as a client to any twitch channel
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
