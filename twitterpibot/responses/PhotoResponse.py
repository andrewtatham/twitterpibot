from Response import Response
import random
import hardware
from TwitterHelper import ReplyWith

class PhotoResponse(Response):
    
    def Condition(self, inboxItem):
        return super(PhotoResponse, self).Condition(inboxItem) \
            and inboxItem.to_me \
            and self.Contains(inboxItem.words, "photo")

    def Respond(self, inboxItem):
        photos = hardware.TakePhotoToDisk("temp", "PhotoResponse", "jpg")
        if any(photos):
            photomessages = ["cheese!", "smile!"]
            ReplyWith(inboxItem=inboxItem, 
                text=random.choice(photomessages), 
                asTweet=True,
                filePaths = photos)


