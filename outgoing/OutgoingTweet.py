
from OutboxTextItem import OutboxTextItem

class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, replyTo = None, text=None , photos=None):

        super(OutgoingTweet, self).__init__();



        if replyTo and replyTo.isTweet and replyTo.status_id :
            self.in_reply_to_status_id = replyTo.status_id
        

      
        self.photos = None
        if photos and any(photos):

            self.photos = photos
            



        self.status = ''

        if replyTo and replyTo.targets:
            for to_screen_name in replyTo.targets:
                self.status = self.status + '@' + to_screen_name + ' '
        elif replyTo and replyTo.sender_screen_name:
                self.status = self.status + '@' + replyTo.sender_screen_name + ' '

        if text:
            self.status = self.status + text

    def Display(args):
        
        
        print("-> Tweet: " + args.status.encode('utf-8'))
