from twitchchatsocket import TwitchChatSocket
from ledconnector import LedConnector

class main:
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'djmoneykey'
    token = 'oauth:46pbz90rxxgmjids6du8at9agwzu47'
    channel = 't4rg3t_d0wn'

    tsc = TwitchChatSocket(server, port, nickname, token, channel)
    #tsc.useWled("http://192.168.1.210")

    #tsc.connect()
    #tsc.useBot()
    #tsc.listen()