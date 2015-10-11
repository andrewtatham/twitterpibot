
from ExceptionHandler import HandleSilently

try:
    import MyPicam
except Exception as e:
    HandleSilently(e)

try:
    import Webcam
except Exception as e:
    HandleSilently(e)

class Cameras(object):
    def __init__(self, *args, **kwargs):
        self._cameras = []
        global hardware          
        if hardware.iswindows:
            for i in range(1):
                try:
                    webcam = Webcam.Webcam(i)
                except Exception as e:
                    HandleSilently(e)
                if webcam:
                    self._cameras.append(webcam)
        else:
            try:
                picam = MyPicam.MyPicam()
            except Exception as e:
                HandleSilently(e)
            if picam:
                self._cameras.append(picam)

    def TakePhotos(args):
        photos=[]

        for camera in args._cameras:
            if camera.enabled:
                photo = camera.TakePhoto()
                if photo :
                    photos.append(photo)

        return photos

    def TakePhotoToDisk(args, dir, name, ext, nightmode):
        filenames=[]
        i = 0
        for camera in args._cameras:
            if camera.enabled:
                name += "_cam_" + "{0:05d}".format(i)
                camera.TakePhotoToDisk(dir, name, ext, nightmode)
                if name:
                    filenames.append(name)
            i += 1
        return filenames


    def CameraFlash(args, on):
        if piglow:
            piglow.CameraFlash(on)
        if brightpi:
            brightpi.CameraFlash(on)


    def Close(args):
        for camera in args._cameras:
            if camera.enabled:
                camera.Close()
