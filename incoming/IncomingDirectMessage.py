from InboxTextItem import InboxTextItem

class IncomingDirectMessage(InboxTextItem):


    def __init__(self, data, context):
        super(IncomingDirectMessage, self).__init__(data)

        self.isDirectMessage = True

        # https://dev.twitter.com/streaming/overview/messages-types#Direct_Messages

        # https://dev.twitter.com/rest/reference/get/direct_messages


        self.sender = context.users.getUser(data = data["direct_message"]["sender"])
        self.recipient = context.users.getUser(data = data["direct_message"]["recipient"])
        self.from_me = self.sender.isMe
        self.to_me = self.recipient.isMe
        self.targets = [self.sender.screen_name]


        self.text = data["direct_message"]["text"]
        self.words = self.text.split()



    def Display(args):
        text = " * DM from @" + args.sender.screen_name + " to @" + args.recipient.screen_name + ": " + args.text.encode('utf-8')
        print(text)
        