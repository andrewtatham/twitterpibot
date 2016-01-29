from twitterpibot.logic import GiphyWrapper
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class GifResponse(Response):
    def condition(self, inbox_item):
        return super(GifResponse, self).condition(inbox_item)

    def respond(self, inbox_item):
        url, path = GiphyWrapper.get_random_gif(inbox_item.text_stripped)
        reply_with(inbox_item=inbox_item,
                   text=url,
                   as_tweet=True,
                   file_paths=[path])
