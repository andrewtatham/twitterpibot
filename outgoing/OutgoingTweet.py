
from OutboxTextItem import OutboxTextItem

class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, replyTo=None, text=None , photos=None, media_id = None, in_reply_to_status_id = None):

        super(OutgoingTweet, self).__init__()

        if in_reply_to_status_id :
            self.in_reply_to_status_id = in_reply_to_status_id
        elif replyTo and replyTo.isTweet and replyTo.status_id :
            self.in_reply_to_status_id = replyTo.status_id
     
        self.photos = None
        if photos and any(photos):
            self.photos = photos

        if media_id:
            self.media_ids = [ media_id ]

        self.status = ''

        if replyTo:
            if replyTo.sender.screen_name:
                self.status += '@' + replyTo.sender.screen_name + ' '
            if replyTo.targets:
                for to_screen_name in replyTo.targets:
                    self.status += '@' + to_screen_name + ' '

        if text:
            self.status = self.status + text

    def Display(args):
        print("-> Tweet: " + args.status)
