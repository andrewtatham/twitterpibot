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

class Context(object):
    def __init__(self, *args, **kwargs):

        self.inbox = Queue()
        self.outbox = Queue()
        self.song = Queue()
        self.users = Users()
        self.ratelimits = RateLimits()
        self.cameras = Cameras()
        
        self.piglow = None
        self.brightpi = None

        self.hardware = Hardware()

        if self.hardware.piglowattached:
            self.piglow = MyPiglow()
        if self.hardware.brightpiattached:
            self.brightpi = MyBrightPi()

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
        status.outboxCount = args.outbox.qsize()
        status.songCount = args.song.qsize()

        status.cpu = psutil.cpu_percent()
        status.memory = psutil.virtual_memory().percent

        return status

class Status(object):
    pass