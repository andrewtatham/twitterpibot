from twitterpibot.responses.Response import Response
import random
import twitterpibot.hardware.hardware as hardware
from twitterpibot.twitter.TwitterHelper import ReplyWith


class PhotoResponse(Response):
    def Condition(self, inbox_item):
        return super(PhotoResponse, self).Condition(inbox_item) \
               and inbox_item.to_me \
               and self.Contains(inbox_item.words, "photo")

    def Respond(self, inbox_item):
        photos = hardware.take_photo("temp", "PhotoResponse", "jpg")
        if any(photos):
            photomessages = ["cheese!", "smile!"]
            ReplyWith(inbox_item=inbox_item,
                      text=random.choice(photomessages),
                      asTweet=True,
                      filePaths=photos)
