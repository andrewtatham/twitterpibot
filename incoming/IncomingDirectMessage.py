from InboxTextItem import InboxTextItem
from IncomingTweet import andrewpiid

class IncomingDirectMessage(InboxTextItem):



    def __init__(self, data):
        # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages

        # https://dev.twitter.com/rest/reference/get/direct_messages

        self.sender_id = str(data["direct_message"]["sender_id_str"])
        self.sender_screen_name = str(data["direct_message"]["sender_screen_name"])
        self.text = str(data["direct_message"]["text"])

        self.words = self.text.split()

        self.recipient_id = str(data["direct_message"]["recipient_id_str"])


        self.from_me = self.sender_id == andrewpiid
        self.to_me = self.recipient_id == andrewpiid

        print("DIRECT MESSAGE: from @" + self.sender_screen_name + ": " + self.text)





    def IsDirectMessage(args):
        return True