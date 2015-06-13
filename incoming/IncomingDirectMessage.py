from InboxTextItem import InboxTextItem
from IncomingTweet import andrewpiid

class IncomingDirectMessage(InboxTextItem):




    def __init__(self, data):
        super(IncomingDirectMessage, self).__init__(data)

        self.isDirectMessage = True

        # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages

        # https://dev.twitter.com/rest/reference/get/direct_messages

        self.sender_id = data["direct_message"]["sender_id_str"]
        self.sender_screen_name = data["direct_message"]["sender_screen_name"]
        self.text = data["direct_message"]["text"]

        self.words = self.text.split()

        self.recipient_id = data["direct_message"]["recipient_id_str"]


        self.from_me = self.sender_id == andrewpiid
        self.to_me = self.recipient_id == andrewpiid
        self.targets = [self.sender_screen_name]


    def Display(args):
        text = " * DM from @" + args.sender_screen_name + ": " + args.text
        print()
        