
from OutboxTextItem import OutboxTextItem

class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, replyTo = None, text=None , media_ids=None):

        super(OutgoingTweet, self).__init__();



        if replyTo is not None and replyTo.isTweet and replyTo.status_id is not None:
            self.in_reply_to_status_id = replyTo.status_id

        if media_ids is not None:
            self.media_ids = media_ids

        self.status = ''

        if replyTo.targets is not None:
            for to_screen_name in replyTo.targets:
                self.status = self.status + '@' + to_screen_name + ' '
        else:
            if replyTo.sender_screen_name is not None:
                self.status = self.status + '@' + replyTo.sender_screen_name + ' '

             
        self.status = self.status + text

    def Display(args):
        
        
        print("-> Tweet: " + args.status)
