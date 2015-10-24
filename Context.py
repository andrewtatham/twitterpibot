
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

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

class Context(object):
    def __init__(self):

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

    def CameraFlash(self, on):

        if self.hardware.piglowattached:
            self.piglow.CameraFlash(on)

        if self.hardware.brightpiattached:
            self.brightpi.CameraFlash(on)

    def OnInboxItemRecieved(self, inboxItem):
        if self.hardware.piglowattached:
            self.piglow.OnInboxItemRecieved(inboxItem)


    def GetStatus(self):

        status = Status()
        status.inboxCount = self.inbox.qsize()

        status.cpu = psutil.cpu_percent()
        status.memory = psutil.virtual_memory().percent

        return status

    def send(self, outboxItem):
        outboxItem.Display()
        response = None
        with MyTwitter() as twitter:
            if type(outboxItem) is OutgoingTweet:
                self.statistics.RecordOutgoingTweet()
                if outboxItem.photos and any(outboxItem.photos):
                    outboxItem.media_ids = twitter.UploadMedia(outboxItem.photos)
                response = twitter.update_status(
                    status = outboxItem.status,
                    in_reply_to_status_id = outboxItem.in_reply_to_status_id,
                    media_ids = outboxItem.media_ids)
            if type(outboxItem) is OutgoingDirectMessage:
                self.statistics.RecordOutgoingDirectMessage()
                response = twitter.send_direct_message(
                    text = outboxItem.text, 
                    screen_name = outboxItem.screen_name, 
                    user_id = outboxItem.user_id)
        id_str = response["id_str"]
        return id_str

class Status(object):
    pass