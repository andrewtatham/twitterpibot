from Queue import Queue
from Cameras import Cameras
from MyPiglow import MyPiglow
import cv2
import os
import tempfile
from Users import Users
from RateLimits import RateLimits
from MyBrightPi import MyBrightPi
from Hardware import Hardware
import psutil
from Statistics import Statistics
from MyTwitter import MyTwitter
from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage

class Context(object):
    def __init__(self, *args, **kwargs):

        self.inbox = Queue()
        self.users = Users()
        
        self.piglow = None
        self.brightpi = None

        self.hardware = Hardware()

        self.cameras = Cameras(self.hardware)


        if self.hardware.piglowattached:
            self.piglow = MyPiglow()
        if self.hardware.brightpiattached:
            self.brightpi = MyBrightPi()
        
        self.statistics = Statistics()

    def CameraFlash(args, on):

        if args.hardware.piglowattached:
            args.piglow.CameraFlash(on)

        if args.hardware.brightpiattached:
            args.brightpi.CameraFlash(on)

    def OnInboxItemRecieved(args, inboxItem):
        if args.hardware.piglowattached:
            args.piglow.OnInboxItemRecieved(inboxItem)


    def GetStatus(args):

        status = Status()
        status.inboxCount = args.inbox.qsize()

        status.cpu = psutil.cpu_percent()
        status.memory = psutil.virtual_memory().percent

        return status

    #def Stop(args):
    #    args.users.Save()


    def send(args, outboxItem):
        if outboxItem:
            outboxItem.Display()

            with MyTwitter() as twitter:
                if type(outboxItem) is OutgoingTweet:
                    if outboxItem.photos and any(outboxItem.photos):
                        outboxItem.media_ids = twitter.UploadMedia(outboxItem.photos)
                    twitter.update_status(
                        status = outboxItem.status,
                        in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                        media_ids = outboxItem.media_ids)
                    args.statistics.RecordOutgoingTweet()
                if type(outboxItem) is OutgoingDirectMessage:
                    twitter.send_direct_message(
                        text = outboxItem.text, 
                        screen_name = outboxItem.screen_name, 
                        user_id = outboxItem.user_id)
                    args.statistics.RecordOutgoingDirectMessage()                    






class Status(object):
    pass