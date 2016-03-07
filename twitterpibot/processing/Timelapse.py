import logging
import datetime
import os
import glob

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
import images2gif

from twitterpibot.logic import fsh
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.hardware

logger = logging.getLogger(__name__)

if twitterpibot.hardware.is_webcam_attached:
    # noinspection PyPackageRequirements,PyUnresolvedReferences
    import cv2


class Timelapse(object):
    def __init__(self, identity, name, start_time, end_time, interval_seconds=1, tweet_text=''):
        self.identity = identity
        self.name = name
        self.imageExtension = 'jpg'
        self.folderName = fsh.root + "temp" + os.path.sep + 'timelapse' + os.path.sep + self.name
        self.dirPath = os.path.abspath(self.folderName)
        self.startTime = start_time
        self.endTime = end_time
        self.intervalSeconds = interval_seconds

        self.initTime = self.startTime + datetime.timedelta(seconds=-1),
        self.uploadTime = self.endTime + datetime.timedelta(seconds=1)

        self.tweetText = tweet_text + " from " + self.startTime.strftime("%X") + " to " + self.endTime.strftime(
            "%X") + " #timelapse"
        self.targetExtension = "gif"  # "mp4" / "gif"
        self.fps = 10
        self.frameDuration = 1.0 / self.fps

        # calculate nuber of frames captured
        duration = self.endTime - self.startTime
        no_of_frames = duration.total_seconds() / self.intervalSeconds

        # expected duration of output video
        duration_seconds = no_of_frames / self.fps

        logger.info("[Timelapse] " + self.name + " Expected duration = " + str(duration_seconds))

        if self.targetExtension == "mp4":
            if duration_seconds < 0.5:
                raise Exception("Video will be too short")
            if duration_seconds > 30:
                raise Exception("Video is too long")

    def get_scheduled_tasks(self):
        tasks = [
            TimelapsePhotoInitTask(self),
            TimelapsePhotoScheduledTask(self),
            TimelapseUploadScheduledTask(self)
        ]
        return tasks


class TimelapsePhotoInitTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapsePhotoInitTask, self).__init__(timelapse.identity)
        self.timelapse = timelapse

    def get_trigger(self):
        return DateTrigger(run_date=self.timelapse.initTime[0])

    def on_run(self):
        logger.info("[Timelapse] Init ")
        fsh.ensure_directory_exists_and_is_empty(self.timelapse.dirPath)


class TimelapsePhotoScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapsePhotoScheduledTask, self).__init__(timelapse.identity)
        self.timelapse = timelapse
        self.i = 0

    def get_trigger(self):
        return IntervalTrigger(
            start_date=self.timelapse.startTime,
            end_date=self.timelapse.endTime,
            seconds=self.timelapse.intervalSeconds
        )

    def on_run(self):
        logger.info("[Timelapse] " + self.timelapse.name + " Photo " + str(self.i))

        name = self.timelapse.name + "_img_" + "{0:05d}".format(self.i)

        twitterpibot.hardware.take_photo(
            folder=self.timelapse.dirPath,
            name=name,
            ext=self.timelapse.imageExtension)

        self.i += 1


class TimelapseUploadScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        super(TimelapseUploadScheduledTask, self).__init__(timelapse.identity)
        self.timelapse = timelapse

    def get_trigger(self):
        return DateTrigger(run_date=self.timelapse.uploadTime)

    def on_run(self):

        search_path = self.timelapse.dirPath + os.path.sep + self.timelapse.name + "*" + os.extsep + self.timelapse.imageExtension

        files = glob.glob(search_path)
        files.sort()
        images = [cv2.imread(file) for file in files]

        filename = self.timelapse.dirPath + os.path.sep + self.timelapse.name + os.extsep + self.timelapse.targetExtension

        if self.timelapse.targetExtension == "gif":

            if twitterpibot.hardware.is_webcam_attached:
                images = [cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) for bgr in images]
            if twitterpibot.hardware.is_picam_attached:
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

            logger.info("[Timelapse] Opening video")
            fourcc = cv2.cv.CV_FOURCC(*'MPG4')
            video = cv2.VideoWriter(
                filenametemp,
                fourcc=fourcc,
                fps=self.timelapse.fps,
                frameSize=(width, height))

            for image in images:
                logger.info("[Timelapse] Writing image to video")
                video.write(image)

            logger.info("[Timelapse] Closing video")
            video.release()

            logger.info("[Timelapse] Renaming video")
            os.rename(filenametemp, filename)

        else:
            raise Exception("Not implemented extension " + self.timelapse.targetExtension)

        logger.info("[Timelapse]" + self.timelapse.name + " Checking")

        if not os.path.isfile(filename):
            raise Exception("File does not exist")

        file_size = os.path.getsize(filename)
        if file_size == 0:
            raise Exception("File size is zero ")

        if (self.timelapse.targetExtension == "gif" and file_size > (5 * 1024 * 1024)) \
                or (self.timelapse.targetExtension == "mp4" and file_size > (15 * 1024 * 1024)):
            raise Exception("File size {0} MB is too big ".format(file_size / (1024 * 1024)))
        logger.info("[Timelapse]" + self.timelapse.name + " Sending")
        self.timelapse.identity.send(OutgoingTweet(
            text=self.timelapse.tweetText,
            file_paths=[filename]))

        fsh.remove_directory_and_contents(self.timelapse.dirPath)
