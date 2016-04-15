import logging

# noinspection PyPackageRequirements
from twitterpibot.logic import magic8ball

from twitterpibot.responses.Response import Response, unmentioned_reply_condition, mentioned_reply_condition

logger = logging.getLogger(__name__)


class Magic8BallResponse(Response):
    def condition(self, inbox_item):
        return (
                   mentioned_reply_condition(inbox_item)
                   or unmentioned_reply_condition(inbox_item)
               ) and "?" in inbox_item.text

    def respond(self, inbox_item):
        response = magic8ball.get_response()
        file_path = None
        if inbox_item.is_tweet:
            file_path = [magic8ball.get_image(response)]
        text = response + " #Magic8Ball"
        self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=text, file_paths=file_path)
