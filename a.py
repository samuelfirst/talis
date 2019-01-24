

import sys
import irc.bot
import requests

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        print("{0}: {1}".format(e.source.split("!")[0], e.arguments[0]))
        return

    def do_command(self, e, cmd):
        c = self.connection


        # The command was not recognized
        #else:
        #    c.privmsg(self.channel, "Did not understand command: " + cmd)

def main():
    (channel,)   = sys.argv[1:]


    HOST_NAME = "irc.chat.twitch.tv"
    PORT = 6667
    BOT_NAME = "talis_jtk"

    f = open('.oauth', 'r')
    OAUTH_TOKEN = f.readline().rstrip(" \n")
    f.close()

    oauth = OAUTH_TOKEN

    print(channel)

    bot = TwitchBot(BOT_NAME, OAUTH_TOKEN, channel)
    bot.start()

if __name__ == "__main__":
    main()
