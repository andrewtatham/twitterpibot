from Response import Response
import cv2
import random
import tempfile
import os





class PhotoResponse(Response):



    
    def Condition(args, inboxItem):
        return super(PhotoResponse, args).Condition(inboxItem) and args.Contains(inboxItem.words, "photo")

    def Respond(args, inboxItem):

        # TOT use Piglow as flash/light

        photos = args.context.cameras.TakePhotos()

        media_ids = []
        for photo in photos:
            if photo is not None and photo.image is not None:

                #temp = tempfile.TemporaryFile(suffix='.jpg')
                
                temp = 'temp.jpg'

                cv2.imwrite(temp, photo.image)
                try:
                    media = args.context.twitter.upload_media(media=open(temp, 'rb'))
                    media_ids.append(media["media_id_string"])
                finally:
                    os.remove(temp)
        
        photomessages = ["cheese!", "smile!"]

        return args.ReplyWith(
            inboxItem=inboxItem, 
            text=random.choice(photomessages), 
            media_ids=media_ids, 
            asTweet=True)


   
        
        