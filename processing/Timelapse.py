from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import datetime
from apscheduler.triggers.date import DateTrigger
import os
import shutil
import glob
import images2gif
import cv2 
from MyTwitter import MyTwitter
from OutgoingTweet import OutgoingTweet

class Timelapse(object):
    def __init__(self, context, name, startTime, endTime, intervalSeconds = 1, tweetText = ''):
        self._context = context
        self.name = name
        self.imageExtension = 'jpg'
        self.folderName = "temp" + os.path.sep + 'timelapse' + os.path.sep + self.name
        self.dirPath = os.path.abspath(self.folderName)
        self.startTime = startTime
        self.endTime = endTime
        self.intervalSeconds = intervalSeconds

        self.initTime = self.startTime + datetime.timedelta(seconds = -1), 
        self.uploadTime = self.endTime + datetime.timedelta(seconds = 1)       

        self.tweetText = tweetText

    def GetScheduledTasks(self):
        tasks = [
            TimelapsePhotoInitTask(self),
            TimelapsePhotoScheduledTask(self),
            TimelapseUploadScheduledTask(self)
        ]
        return tasks

class TimelapsePhotoInitTask(ScheduledTask):
    def __init__(self, timelapse):
        self.timelapse = timelapse
    def GetTrigger(args):
        return DateTrigger(run_date = args.timelapse.initTime[0])
    def onRun(args):
        print("[Timelapse] Init ")
        if os.path.exists(args.timelapse.dirPath):
            print("[Timelapse] Removing " + args.timelapse.dirPath)
            shutil.rmtree(args.timelapse.dirPath, True)
        if not os.path.exists(args.timelapse.dirPath):
            print("[Timelapse] Creating " + args.timelapse.dirPath)
            os.makedirs(args.timelapse.dirPath)
        


class TimelapsePhotoScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        self.timelapse = timelapse
        self.i = 0
    def GetTrigger(args):
        return IntervalTrigger(
            start_date = args.timelapse.startTime,
            end_date = args.timelapse.endTime,
            seconds = args.timelapse.intervalSeconds
            )
    def onRun(args):
        print("[Timelapse] Photo " + str(args.i))

        name = args.timelapse.name + "_img_"  + "{0:05d}".format(args.i)

        args.context.cameras.TakePhotoToDisk(
            dir = args.timelapse.dirPath,
            name = name,
            ext = args.timelapse.imageExtension
            ) 

        args.i += 1
        

class TimelapseUploadScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        self.timelapse = timelapse
    def GetTrigger(args):
        return DateTrigger(run_date = args.timelapse.uploadTime)
    def onRun(args):


        # TODO handle multiple cameras

        searchPath = args.timelapse.dirPath + os.path.sep + args.timelapse.name + "*" + os.extsep + args.timelapse.imageExtension

        print("[Timelapse] Creating GIF")
        files = glob.glob(searchPath)

        imagesBGR = [cv2.imread(file) for file in files]
        imagesRGB = [cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) for bgr in imagesBGR ]
        filename = args.timelapse.dirPath + os.path.sep + args.timelapse.name + ".gif"

        images2gif.writeGif(
            filename, 
            imagesRGB,
            dither = True, 
            duration = 0.1, 
            repeat = True, 
            subRectangles = None)


        print("[Timelapse] Uploading")
        with MyTwitter() as twitter:
            media_id = twitter.UploadMediaFromDisk(filename)

            args.context.outbox.put(OutgoingTweet(
                text = args.timelapse.tweetText,
                media_id = media_id))

        if os.path.exists(args.timelapse.dirPath):
            print("[Timelapse] Removing " + args.timelapse.dirPath)
            shutil.rmtree(args.timelapse.dirPath, True)
