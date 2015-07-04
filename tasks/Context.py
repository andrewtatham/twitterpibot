from Queue import Queue
from Cameras import Cameras
from MyPiglow import MyPiglow
import cv2
import os
import tempfile
class Context(object):
    def __init__(self, *args, **kwargs):
        self.inbox = Queue()
        self.outbox = Queue()
        self.song = Queue()


        self.cameras = Cameras()
        self.piglow = MyPiglow()

    def GetStatus(args):

        status = Status()
        status.inboxCount = args.inbox.qsize()
        status.outboxCount = args.outbox.qsize()
        status.songCount = args.song.qsize()

        return status

    def UploadMedia(args, photos):
        media_ids = []
        for photo in photos:
            if photo and photo.image is not None :
                try:
                    temp = tempfile.TemporaryFile(suffix='.jpg',delete=False)

       

                    print('saving ' + temp.name)
                    cv2.imwrite(temp.name, photo.image)

                    temp.file.seek(0)
                    
                    if not temp.close_called:
                        temp.close()

                    try:
                        f = open(temp.name,'rb')

                        print('uploading')
                        media = args.twitter.upload_media(media=f)
                        media_id =  media["media_id_string"]
                        if media_id :
                            print('media_id = ' + media_id)
                            media_ids.append(media_id)
                    finally:
                        if not f.closed:
                                    f.close() 
                finally:
               
                   
                    if not temp.close_called:
                        temp.close()
                    #print('removing ' + temp)
                    os.remove(temp.name)
        
        return media_ids
class Status(object):
    pass