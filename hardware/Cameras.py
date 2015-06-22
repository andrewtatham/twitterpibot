
from MyPicam import MyPicam
from Webcam import Webcam
class Cameras(object):
    def __init__(self, *args, **kwargs):
        self.cameras = []


        picam = MyPicam()
        if picam.enabled:
            self.cameras.append(picam)
            

        for i in range(3):
            webcam = Webcam(i)
            if webcam.enabled:
                self.cameras.append(webcam)

    def TakePhotos(args):
        photos=[]

        for camera in args.cameras:
            if camera.enabled:
                photo = camera.TakePhoto()
                if photo :
                    photos.append(photo)

        return photos


    def Close(args):
        for camera in args.cameras:
            if camera.enabled:
                camera.Close()
