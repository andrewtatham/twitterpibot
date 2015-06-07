from OutboxTextItem import OutboxTextItem

class OutgoingDirectMessage(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, context, dmText):
        

        self.screen_name = context.to
        self.text = dmText
         
