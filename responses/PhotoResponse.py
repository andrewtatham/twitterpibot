from Response import Response
import random
import hardware
from TwitterHelper import ReplyWith

class PhotoResponse(Response):
    
    def Condition(args, inboxItem):
        return super(PhotoResponse, args).Condition(inboxItem) \
            and inboxItem.to_me \
            and args.Contains(inboxItem.words, "photo")

    def Respond(args, inboxItem):
        photos = hardware.TakePhotoToDisk("temp", "PhotoResponse", "jpg")
        if any(photos):
            photomessages = ["cheese!", "smile!"]
            ReplyWith(inboxItem=inboxItem, 
                text=random.choice(photomessages), 
                asTweet=True,
                filePaths = photos)


