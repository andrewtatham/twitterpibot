import random

from twitterpibot.logic import giphyhelper, FatherTed
from twitterpibot.responses.Response import Response, mentioned_reply_condition


class GifResponse(Response):
    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) and inbox_item.is_tweet

    def respond(self, inbox_item):
        response = random.choice(FatherTed.responses)
        gif = giphyhelper.get_random_gif(screen_name=self.identity.screen_name, text=inbox_item.text_stripped)
        file_paths = [gif]
        self.identity.twitter.reply_with(
            inbox_item=inbox_item,
            text=response,
            file_paths=file_paths)
