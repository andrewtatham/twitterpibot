from InboxTextItem import InboxTextItem
class IncomingDirectMessage(InboxTextItem):
    def __init__(self, data):
        # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages

        # https://dev.twitter.com/rest/reference/get/direct_messages

        self.sender_id = str(data["direct_message"]["sender_id_str"])
        self.sender_screen_name = str(data["direct_message"]["sender_screen_name"])
        self.text = str(data["direct_message"]["text"])
        print("DIRECT MESSAGE: from @" + self.sender_screen_name + ": " + self.text)



    def NeedsReply(self):
        return True