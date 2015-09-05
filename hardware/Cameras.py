
from MyPicam import MyPicam
from Webcam import Webcam
class Cameras(object):
    def __init__(self, *args, **kwargs):
        self.cameras = []


        picam = MyPicam()
        if picam.enabled:
            self.cameras.append(picam)
            

        for i in range(1):
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

    def TakePhotoToDisk(args, dir, name, ext):
        filenames=[]
        i = 0
        for camera in args.cameras:
            if camera.enabled:
                name += "_cam_" + "{0:05d}".format(i)
                camera.TakePhotoToDisk(dir, name, ext)
                if name:
                    filenames.append(name)
            i += 1
        return filenames


    def Close(args):
        for camera in args.cameras:
            if camera.enabled:
                camera.Close()
