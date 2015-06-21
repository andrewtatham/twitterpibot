from Response import Response
import cv2
import random
import tempfile
import os





class PhotoResponse(Response):



    
    def Condition(args, inboxItem):
        return super(PhotoResponse, args).Condition(inboxItem) and args.Contains(inboxItem.words, "photo")

    def Respond(args, inboxItem):

        
        args.context.piglow.CameraFlash(True)

        photos = args.context.cameras.TakePhotos()

        args.context.piglow.CameraFlash(False)

        media_ids = args.context.UploadMedia(photos)

        
        photomessages = ["cheese!", "smile!"]

        return args.ReplyWith(
            inboxItem=inboxItem, 
            text=random.choice(photomessages), 
            media_ids=media_ids, 
            asTweet=True)


