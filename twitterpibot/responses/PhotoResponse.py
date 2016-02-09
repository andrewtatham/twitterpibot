from twitterpibot.responses.Response import Response
import random
import twitterpibot.hardware.hardware as hardware
from twitterpibot.twitter.TwitterHelper import reply_with


class PhotoResponse(Response):
    def condition(self, inbox_item):
        return super(PhotoResponse, self).reply_condition(inbox_item) \
               and "photo" in inbox_item.words

    def respond(self, inbox_item):
        photos = hardware.take_photo("temp", "PhotoResponse", "jpg")
        if any(photos):
            messages = ["cheese!", "smile!"]
            reply_with(inbox_item=inbox_item,
                       text=random.choice(messages),
                       as_tweet=True,
                       file_paths=photos)
