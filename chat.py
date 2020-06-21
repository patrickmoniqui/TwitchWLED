class Chat:
    TWITCH_CHAT_CHAR_LIMIT = 500

    @staticmethod
    def maximumEmote(emoteName):
        str = ""
        while len(str) + (len(emoteName)+1) <= Chat.TWITCH_CHAT_CHAR_LIMIT:
            str += emoteName + " "
        return str