from OutboxTextItem import OutboxTextItem


class OutgoingDirectMessage(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, reply_to=None, text=None, user_id=None, screen_name=None):

        super(OutgoingDirectMessage, self).__init__()
        if reply_to:
            self.user_id = reply_to.sender.id
            self.screen_name = reply_to.sender.screen_name
        else:
            self.user_id = user_id
            self.screen_name = screen_name

        self.text = text

    def Display(self):
        print(u"-> DM to @" + self.screen_name + u": " + self.text)
