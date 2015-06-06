from Task import Task

try:
    import cv2
    import urllib
    import numpy as np
except Exception:
    enableImages = False


class DisplayImagesTask(Task):

    def onInit(args):
        cv2.startWindowThread()
        cv2.waitKey(1)

        windowname = "Image"
        window = cv2.namedWindow(windowname)

    def onRun(args):
        image = imageQueue.get()
        imageQueue.task_done()
        cv2.imshow(windowname, image)
        cv2.waitKey(1)
        time.sleep(2)

        pass


def DisplayImages():

    while running:

  
def OnStop(args):
    cv2.destroyWindow(windowname)

    def DownloadImage(url):
   
    retval = urllib.urlretrieve(url)
    while(not os.path.isfile(retval[0])):
        time.sleep(0.25)
    return retval[0]
        
def ShowImage(path, text):
    if(os.path.isfile(path)):
        image = cv2.imread(path,0)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        scale = 0.75
        origin = (10,20)
        text = textwrap.wrap(text,50)
        for line in text:
            cv2.putText(image,line,origin, font, scale,(0,0,0),3,cv2.CV_AA)
            cv2.putText(image,line,origin, font, scale,(255,255,255),1,cv2.CV_AA)
            origin = (origin[0],origin[1] + 20)
        # actually we queue it now
        imageQueue.put(image)

