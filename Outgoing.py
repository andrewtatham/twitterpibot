class OutgoingDirectMessage(OutboxItem):
    # https://dev.twitter.com/rest/reference/post/direct_messages/new
    def __init__(self, context, dmText):
        

        self.screen_name = context.to
        self.text = dmText
         



def ReplyWith(context, replyText):    
    if context.isTweet:
        tweet = OutgoingTweet(context, replyText)
        outbox.put(tweet)
    if context.isDirectMessage:
        dm = OutgoingDirectMessage(context, replyText)
        outbox.put(dm)


class OutboxItem(object):
    pass

class OutgoingTweet(OutboxItem):
    # https://dev.twitter.com/rest/reference/post/statuses/update

    def __init__(self, context, tweetText):

        if context.status_id is not None:
            self.in_reply_to_status_id = context.status_id

        if context.media_ids is not None:
            self.media_ids = context.media_ids

        self.status = ''
        if context.to_screen_name is not None:
            self.status = self.status + '@' + context.to_screen_name + ' '

        if context.to_screen_names is not None:
            for to_screen_name in context.to_screen_names:
                self.status = self.status + '@' + to_screen_name + ' '
             
        self.status = self.status + tweetText
