from InboxTextItem import InboxTextItem
import Users

class IncomingDirectMessage(InboxTextItem):


    def __init__(self, data):
        super(IncomingDirectMessage, self).__init__()

        self.isDirectMessage = True

        # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages

        # https://dev.twitter.com/rest/reference/get/direct_messages


        self.sender = Users.getUser(data = data["direct_message"]["sender"])
        self.recipient = Users.getUser(data = data["direct_message"]["recipient"])
        self.from_me = self.sender.isMe
        self.to_me = self.recipient.isMe
        self.targets = [self.sender.screen_name]


        self.text = data["direct_message"]["text"]
        self.words = self.text.split()



    def Display(self):
        text = u" * DM from @" + self.sender.screen_name + u" to @" + self.recipient.screen_name + u": " + self.text
        print(text)
        