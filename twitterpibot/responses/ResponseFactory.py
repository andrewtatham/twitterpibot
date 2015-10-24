import twitterpibot.Identity as Identity
from twitterpibot.twitter.MyTwitter import MyTwitter


class ResponseFactory(object):
    def __init__(self):
        self.responses = Identity.get_responses()
        for response in self.responses:
            print("[ResponseFactory] adding " + str(type(response)))

    def Create(self, inbox_item):
        if inbox_item:
            for response in self.responses:
                if response.Condition(inbox_item):

                    inbox_item.isRespondedTo = True

                    if inbox_item.isTweet and not inbox_item.favorited and not inbox_item.from_me and response.Favourite(
                            inbox_item):
                        with MyTwitter() as twitter:
                            twitter.create_favourite(id=inbox_item.status_id)

                    response.Respond(inbox_item)
        return None
