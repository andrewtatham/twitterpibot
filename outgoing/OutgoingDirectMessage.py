from OutboxTextItem import OutboxTextItem

class OutgoingDirectMessage(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, inboxItem, text):
        

        self.user_id = inboxItem.sender_id
        self.sender_screen_name = inboxItem.sender_screen_name
        self.text = text
         
    def Display(args):
        
        
        print(args.text)