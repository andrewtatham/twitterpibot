import random
from twitterpibot.logic import GiphyWrapper
from twitterpibot.processing import FatherTed
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class GifResponse(Response):
    def condition(self, inbox_item):
        return super(GifResponse, self).reply_condition(inbox_item) and inbox_item.is_tweet

    def respond(self, inbox_item):
        response = random.choice(FatherTed.responses)
        file_paths = [GiphyWrapper.get_random_gif(inbox_item.text_stripped)]
        reply_with(inbox_item=inbox_item,
                   text=response,
                   file_paths=file_paths)
