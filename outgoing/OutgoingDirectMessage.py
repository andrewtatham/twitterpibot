from OutboxTextItem import OutboxTextItem

class OutgoingDirectMessage(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, replyTo, text):
        
        super(OutgoingDirectMessage, self).__init__()

        self.user_id = replyTo.sender.id
        self.screen_name = replyTo.sender.screen_name
        self.text = text
         
    def Display(args):
        print(unicode(u"-> DM to @" + unicode(args.screen_name) + u": " + unicode(args.text)))