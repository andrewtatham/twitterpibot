from Queue import Queue
from Cameras import Cameras
from MyPiglow import MyPiglow
import cv2
import os
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
            if photo is not None and photo.image is not None:

                #temp = tempfile.TemporaryFile(suffix='.jpg').name
                
                temp = 'temp.jpg'

                print('saving ' + temp)
                cv2.imwrite(temp, photo.image)
                try:
                    print('opening ' + temp)
                    file = open(temp, 'rb')
                    print('uploading')
                    media = args.twitter.upload_media(media=file)
                    print('media_id = ' + media["media_id_string"])
                    media_ids.append(media["media_id_string"])
                finally:
                    print('removing ' + temp)
                    os.remove(temp)
        
        return media_ids
class Status(object):
    pass