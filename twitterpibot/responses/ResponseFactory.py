import twitterpibot.Identity as Identity
import logging
from twitterpibot.twitter import TwitterHelper
logger = logging.getLogger(__name__)

class ResponseFactory(object):
    def __init__(self):
        self.responses = Identity.get_responses()
        for response in self.responses:
            logger.info("[ResponseFactory] adding " + str(type(response)))

    def Create(self, inbox_item):
        if inbox_item:
            for response in self.responses:
                if response.Condition(inbox_item):

                    inbox_item.isRespondedTo = True

                    if inbox_item.isTweet \
                        and not inbox_item.favorited \
                        and not inbox_item.from_me \
                        and response.Favourite(inbox_item):
                        TwitterHelper.create_favourite(inbox_item.status_id)

                    response.Respond(inbox_item)
        return None
