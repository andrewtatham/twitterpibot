
from MyPicam import MyPicam
from Webcam import Webcam
class Cameras(object):
    def __init__(self, hardware, *args, **kwargs):
        self.cameras = []
            
        if hardware.iswindows:
            for i in range(1):
                webcam = Webcam(i)
                if webcam.enabled:
                    self.cameras.append(webcam)
        else:
            picam = MyPicam()
            if picam.enabled:
                self.cameras.append(picam)

    def TakePhotos(args):
        photos=[]

        for camera in args.cameras:
            if camera.enabled:
                photo = camera.TakePhoto()
                if photo :
                    photos.append(photo)

        return photos

    def TakePhotoToDisk(args, dir, name, ext, nightmode):
        filenames=[]
        i = 0
        for camera in args.cameras:
            if camera.enabled:
                name += "_cam_" + "{0:05d}".format(i)
                camera.TakePhotoToDisk(dir, name, ext, nightmode)
                if name:
                    filenames.append(name)
            i += 1
        return filenames


    def Close(args):
        for camera in args.cameras:
            if camera.enabled:
                camera.Close()
