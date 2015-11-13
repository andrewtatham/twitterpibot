from twitterpibot.responses.Response import Response
import random
import twitterpibot.hardware.hardware as hardware
from twitterpibot.twitter.TwitterHelper import reply_with


class PhotoResponse(Response):
    def condition(self, inbox_item):
        return super(PhotoResponse, self).condition(inbox_item) \
               and inbox_item.to_me \
               and "photo" in inbox_item.words

    def respond(self, inbox_item):
        photos = hardware.take_photo("temp", "PhotoResponse", "jpg")
        if any(photos):
            photomessages = ["cheese!", "smile!"]
            reply_with(inbox_item=inbox_item,
                       text=random.choice(photomessages),
                       as_tweet=True,
                       file_paths=photos)
