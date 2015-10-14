
import hardware
import Identity

class ResponseFactory(object):
    def __init__(self, *args, **kwargs):
        self.responses = Identity.GetResponses()

    def Create(args, inboxItem):
        if inboxItem :
            for response in args.responses:
                if response.Condition(inboxItem):

                    inboxItem.isRespondedTo = True

                    if inboxItem.isTweet and not inboxItem.favorited and response.Favourite(inboxItem):
                        with MyTwitter() as twitter:
                            twitter.create_favourite(id = inboxItem.status_id)

                    response.Respond(inboxItem)
        return None
        
