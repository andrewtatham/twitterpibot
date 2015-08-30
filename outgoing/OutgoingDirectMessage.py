from OutboxTextItem import OutboxTextItem

class OutgoingDirectMessage(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, replyTo, text):
        
        super(OutgoingDirectMessage, self).__init__()

        self.user_id = replyTo.sender_id
        self.screen_name = replyTo.sender_screen_name
        self.text = text
         
    def Display(args):
        print("-> DM to @" + args.screen_name + ": " + args.text.encode('utf-8'))