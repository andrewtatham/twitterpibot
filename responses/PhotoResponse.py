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
        
        #args.context.piglow.CameraFlash(True)

        photos = args.context.cameras.TakePhotos()

        #args.context.piglow.CameraFlash(False)


        media_ids = []
        for photo in photos:
            if photo is not None and photo.image is not None:

                #temp = tempfile.TemporaryFile(suffix='.jpg').name
                
                temp = 'temp.jpg'

                print('saving ' + temp)
                cv2.imwrite(temp, photo.image)
                try:
                    print('opening ' + temp)
                    file = open(temp, 'rb')
                    print('uploading')
                    media = args.context.twitter.upload_media(media=file)
                    print('media_id = ' + media["media_id_string"])
                    media_ids.append(media["media_id_string"])
                finally:
                    print('removing ' + temp)
                    os.remove(temp)
        
        photomessages = ["cheese!", "smile!"]

        return args.ReplyWith(
            inboxItem=inboxItem, 
            text=random.choice(photomessages), 
            media_ids=media_ids, 
            asTweet=True)


   
        
        