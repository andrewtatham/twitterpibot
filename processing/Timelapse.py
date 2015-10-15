from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import datetime
from apscheduler.triggers.date import DateTrigger
import os
import shutil
import glob
import images2gif
import cv2 

from OutgoingTweet import OutgoingTweet
from TwitterHelper import Send
import hardware

class Timelapse(object):
    def __init__(self, name, startTime, endTime, intervalSeconds = 1, tweetText = ''):
        self.name = name
        self.imageExtension = 'jpg'
        self.folderName = "temp" + os.path.sep + 'timelapse' + os.path.sep + self.name
        self.dirPath = os.path.abspath(self.folderName)
        self.startTime = startTime
        self.endTime = endTime
        self.intervalSeconds = intervalSeconds

        self.initTime = self.startTime + datetime.timedelta(seconds = -1), 
        self.uploadTime = self.endTime + datetime.timedelta(seconds = 1)       

        self.tweetText = tweetText  + " from " + self.startTime.strftime("%X") + " to " + self.endTime.strftime("%X") + " #timelapse"
        self.targetExtension = "gif" # "mp4" / "gif"
        self.fps = 10
        self.frameDuration = 1.0 / self.fps


        # calculate nuber of frames captured
        duration = self.endTime - self.startTime
        noFrames = duration.total_seconds() / self.intervalSeconds

        ## expected duration of output video
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

        print("[Timelapse] " + args.timelapse.name + " Photo " + str(args.i))

        name = args.timelapse.name + "_img_"  + "{0:05d}".format(args.i)

        hardware.TakePhotoToDisk(
            dir = args.timelapse.dirPath,
            name = name,
            ext = args.timelapse.imageExtension) 

        args.i += 1
        

class TimelapseUploadScheduledTask(ScheduledTask):
    def __init__(self, timelapse):
        self.timelapse = timelapse
    def GetTrigger(args):
        return DateTrigger(run_date = args.timelapse.uploadTime)
    def onRun(args):




        searchPath = args.timelapse.dirPath + os.path.sep + args.timelapse.name + "*" + os.extsep + args.timelapse.imageExtension

        files = glob.glob(searchPath)
        files.sort()
        images = [cv2.imread(file) for file in files]

        filename = args.timelapse.dirPath + os.path.sep + args.timelapse.name + os.extsep + args.timelapse.targetExtension

        if args.timelapse.targetExtension == "gif":

            if hardware.iswebcamattached:
                images = [cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB) for bgr in images ]
            if hardware.ispicamattached:
                images = [cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) for bgr in images ]

            images2gif.writeGif(
                filename, 
                images,
                dither = True, 
                duration = args.timelapse.frameDuration, 
                repeat = True, 
                subRectangles = None)

        elif args.timelapse.targetExtension == "mp4":
            #height , width , layers =  images[0].shape
            width = 640
            height = 480

            filenametemp = args.timelapse.dirPath + os.path.sep + args.timelapse.name + os.extsep + "avi"


            print("[Timelapse] Opening video")
            fourcc = cv2.cv.CV_FOURCC(*'MPG4')
            video = cv2.VideoWriter(
                filenametemp,
                fourcc = fourcc,
                fps = args.timelapse.fps,
                frameSize = (width,height))

            for image in images:
                print("[Timelapse] Writing image to video")
                video.write(image)

            print("[Timelapse] Closing video")
            video.release()

            print("[Timelapse] Renaming video")
            os.rename(filenametemp,filename)

        else:
            raise Exception("Not implemented extension " + args.timelapse.targetExtension)

        print("[Timelapse]" + args.timelapse.name + " Checking")

        if not os.path.isfile(filename):
            raise Exception("File does not exist")    

        fileSize = os.path.getsize(filename)
        if fileSize == 0:
            raise Exception("File size is zero ")


        if (args.timelapse.targetExtension == "gif" and fileSize > (4 * 1024 * 1024)) \
            or (args.timelapse.targetExtension == "mp4" and fileSize > (15 * 1024 * 1024)):
            raise Exception("File size is too big ")


        print("[Timelapse]" + args.timelapse.name + " Sending")
        Send(OutgoingTweet(
            text = args.timelapse.tweetText,
            filePaths = [ filename ]))

        if os.path.exists(args.timelapse.dirPath):
            print("[Timelapse] Removing " + args.timelapse.dirPath)
            shutil.rmtree(args.timelapse.dirPath, True)
