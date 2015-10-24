import twitterpibot.Identity as Identity
from twitterpibot.twitter.MyTwitter import MyTwitter


class ResponseFactory(object):
    def __init__(self):
        self.responses = Identity.GetResponses()
        for response in self.responses:
            print("[ResponseFactory] adding " + str(type(response)))

    def Create(self, inboxItem):
        if inboxItem:
            for response in self.responses:
                if response.Condition(inboxItem):

                    inboxItem.isRespondedTo = True

                    if inboxItem.isTweet and not inboxItem.favorited and not inboxItem.from_me and response.Favourite(
                            inboxItem):
                        with MyTwitter() as twitter:
                            twitter.create_favourite(id=inboxItem.status_id)

                    response.Respond(inboxItem)
        return None
