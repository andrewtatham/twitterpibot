from apscheduler.triggers.interval import IntervalTrigger
import datetime
from apscheduler.triggers.date import DateTrigger
import os
import shutil
import glob
import images2gif
# noinspection PyPackageRequirements,PyUnresolvedReferences
import cv2

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.twitter.TwitterHelper import send
import twitterpibot.hardware.hardware as hardware


class Timelapse(object):
    def __init__(self, name, startTime, endTime, intervalSeconds=1, tweetText=''):
        self.name = name
        self.imageExtension = 'jpg'
        self.folderName = "temp" + os.path.sep + 'timelapse' + os.path.sep + self.name
        self.dirPath = os.path.abspath(self.folderName)
        self.startTime = startTime
        self.endTime = endTime
        self.intervalSeconds = intervalSeconds

        self.initTime = self.startTime + datetime.timedelta(seconds=-1),
        self.uploadTime = self.endTime + datetime.timedelta(seconds=1)

        self.tweetText = tweetText + " from " + self.startTime.strftime("%X") + " to " + self.endTime.strftime(
            "%X") + " #timelapse"
        self.targetExtension = "gif"  # "mp4" / "gif"
        self.fps = 10
        self.frameDuration = 1.0 / self.fps

        # calculate nuber of frames captured
        duration = self.endTime - self.startTime
        noFrames = duration.total_seconds() / self.intervalSeconds

        # expected duration of output video
        durationSeconds = noFrames / self.fps

        print("[Timelapse] " + self.name + " Expected duration = " + str(durationSeconds))

        if self.targetExtension == "mp4":
            if durationSeconds < 0.5:
                raise Exception("Video will be too short")
            if durationSeconds > 30:
                raise Exception("Video is too long")

    def GetScheduledTasks(self):
        tasks = [
            TimelapsePhotoInitTask(self),
            TimelapsePhotoScheduledTask(self),
            TimelapseUploadScheduledTask(self)
        ]
        return tasks


class TimelapsePhotoInitTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapsePhotoInitTask, self).__init__()
        self.timelapse = timelapse

    def GetTrigger(self):
        return DateTrigger(run_date=self.timelapse.initTime[0])

    def onRun(self):
        print("[Timelapse] Init ")
        if os.path.exists(self.timelapse.dirPath):
            print("[Timelapse] Removing " + self.timelapse.dirPath)
            shutil.rmtree(self.timelapse.dirPath, True)
        if not os.path.exists(self.timelapse.dirPath):
            print("[Timelapse] Creating " + self.timelapse.dirPath)
            os.makedirs(self.timelapse.dirPath)


class TimelapsePhotoScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapsePhotoScheduledTask, self).__init__()
        self.timelapse = timelapse
        self.i = 0

    def GetTrigger(self):
        return IntervalTrigger(
            start_date=self.timelapse.startTime,
            end_date=self.timelapse.endTime,
            seconds=self.timelapse.intervalSeconds
        )

    def onRun(self):
        print("[Timelapse] " + self.timelapse.name + " Photo " + str(self.i))

        name = self.timelapse.name + "_img_" + "{0:05d}".format(self.i)

        hardware.take_photo(
            dir=self.timelapse.dirPath,
            name=name,
            ext=self.timelapse.imageExtension)

        self.i += 1


class TimelapseUploadScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapseUploadScheduledTask, self).__init__()
        self.timelapse = timelapse

    def GetTrigger(self):
        return DateTrigger(run_date=self.timelapse.uploadTime)

    def onRun(self):

        searchPath = self.timelapse.dirPath + os.path.sep + self.timelapse.name + "*" + os.extsep + self.timelapse.imageExtension

        files = glob.glob(searchPath)
        files.sort()
        images = [cv2.imread(file) for file in files]

        filename = self.timelapse.dirPath + os.path.sep + self.timelapse.name + os.extsep + self.timelapse.targetExtension

        if self.timelapse.targetExtension == "gif":

            if hardware.is_webcam_attached:
                images = [cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) for bgr in images]
            if hardware.is_picam_attached:
                images = [cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) for bgr in images]

            images2gif.writeGif(
                filename,
                images,
                dither=True,
                duration=self.timelapse.frameDuration,
                repeat=True,
                subRectangles=None)

        elif self.timelapse.targetExtension == "mp4":
            # height , width , layers =  images[0].shape
            width = 640
            height = 480

            filenametemp = self.timelapse.dirPath + os.path.sep + self.timelapse.name + os.extsep + "avi"

            print("[Timelapse] Opening video")
            fourcc = cv2.cv.CV_FOURCC(*'MPG4')
            video = cv2.VideoWriter(
                filenametemp,
                fourcc=fourcc,
                fps=self.timelapse.fps,
                frameSize=(width, height))

            for image in images:
                print("[Timelapse] Writing image to video")
                video.write(image)

            print("[Timelapse] Closing video")
            video.release()

            print("[Timelapse] Renaming video")
            os.rename(filenametemp, filename)

        else:
            raise Exception("Not implemented extension " + self.timelapse.targetExtension)

        print("[Timelapse]" + self.timelapse.name + " Checking")

        if not os.path.isfile(filename):
            raise Exception("File does not exist")

        fileSize = os.path.getsize(filename)
        if fileSize == 0:
            raise Exception("File size is zero ")

        if (self.timelapse.targetExtension == "gif" and fileSize > (4 * 1024 * 1024)) \
                or (self.timelapse.targetExtension == "mp4" and fileSize > (15 * 1024 * 1024)):
            raise Exception("File size is too big ")

        print("[Timelapse]" + self.timelapse.name + " Sending")
        send(OutgoingTweet(
            text=self.timelapse.tweetText,
            filePaths=[filename]))

        if os.path.exists(self.timelapse.dirPath):
            print("[Timelapse] Removing " + self.timelapse.dirPath)
            shutil.rmtree(self.timelapse.dirPath, True)
