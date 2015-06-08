
from OutboxTextItem import OutboxTextItem

class OutgoingTweet(OutboxTextItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, inboxItem , text, media_ids = None):

        if inboxItem is not None and inboxItem.IsTweet() and inboxItem.status_id is not None:
            self.in_reply_to_status_id = inboxItem.status_id

        #if media_ids is not None and media_ids:
        self.media_ids = media_ids

        self.status = ''

        if inboxItem.targets is not None:
            for to_screen_name in inboxItem.targets:
                self.status = self.status + '@' + to_screen_name + ' '


        if inboxItem.sender_screen_name is not None:
            self.status = self.status + '@' + inboxItem.sender_screen_name + ' '

             
        self.status = self.status + text

    def Display(args):
        
        
        print("-> Tweet: " + args.status)
