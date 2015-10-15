
import hardware
import Identity

class ResponseFactory(object):
    def __init__(self, *args, **kwargs):
        self.responses = Identity.GetResponses()
        for response in self.responses:
            print("[ResponseFactory] adding " + str(type(response)))

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
        
