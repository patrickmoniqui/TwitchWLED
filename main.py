from twitchchatsocket import TwitchChatSocket
from streamlabsocket import StreamlabSocket
from wledconnector import WledConnector

class main:
    # Infos
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'djmoneykey'
    TwitchChatToken = 'oauth:46pbz90rxxgmjids6du8at9agwzu47'
    #TwitchChatToken = 'oauth:tt0yvnrm291tb7gb3pb2ig74kizp5x'
    Channel = 'djmoneykey'
    StreamlabSocketToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjgwOUFFMUMyQ0U1NzNEMkM0N0ZBIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNTAzODgzOTM2IiwiZmFjZWJvb2tfaWQiOiIxMDE1ODAxMjAzNTM3MTM1MiJ9.iYBMaNu7Mo__9-R-JytZLG-vToEuwJqIFwEwlm3GwLg' #Socket token from /socket/token end point
    WledIps = ['http://192.168.0.210', 'http://192.168.0.211', 'http://192.168.0.212', 'http://192.168.0.213']
    #WledIps = ['http://192.168.0.210']
    #WledIps = None

    wled = None
    if WledIps:
        wled = WledConnector.getInstance()
        wled.setup(WledIps)

    # Twitch Chat
    tcs = TwitchChatSocket(server, port, nickname, TwitchChatToken, Channel)

    try: 
        tcs
        if wled:
            tcs.useWled(wled)

        #tcs.useUI()
        tcsThread = tcs.listen()
    except:
        print("Twitch not used")
    
    # Streamlab Events
    ss = StreamlabSocket(StreamlabSocketToken)

    try:
        ss
        if wled:
            ss.useWled(wled)

        ssThread = ss.listen()
    except:
        print("Streamlab not used")

    # Wait for threads
    try:
        ssThread
        ssThread.join()
    except:
        print("")
    
    try:
        tcsThread
        tcsThread.join()
    except:
        print("")