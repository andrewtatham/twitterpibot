import random

from twitterpibot.logic import GiphyWrapper
from twitterpibot.processing import FatherTed
from twitterpibot.responses.Response import Response


class GifResponse(Response):
    def condition(self, inbox_item):
        return super(GifResponse, self).reply_condition(inbox_item) and inbox_item.is_tweet

    def respond(self, inbox_item):
        response = random.choice(FatherTed.responses)
        gif = GiphyWrapper.get_random_gif(screen_name=self.identity.screen_name, text=inbox_item.text_stripped)
        file_paths = [gif]
        self.identity.twitter.reply_with(
            inbox_item=inbox_item,
            text=response,
            file_paths=file_paths)
