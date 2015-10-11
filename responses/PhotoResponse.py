from Response import Response
import cv2
import random
import tempfile
import os

class PhotoResponse(Response):
    
    def Condition(args, inboxItem):
        return super(PhotoResponse, args).Condition(inboxItem) \
            and inboxItem.to_me \
            and args.Contains(inboxItem.words, "photo")

    def Respond(args, inboxItem):
        
        CameraFlash(True)
        photos = cameras.TakePhotos()
        CameraFlash(False)
        
        if any(photos):
            photomessages = ["cheese!", "smile!"]
            ReplyWith(inboxItem=inboxItem, 
                text=random.choice(photomessages), 
                asTweet=True,
                photos = photos)


