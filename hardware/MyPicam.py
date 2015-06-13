
from Camera import Camera, Photo
import time

enablePicam = True

try:
    import picamera
    import picamera.array
except Exception:
    enablePicam = False


class MyPicam(Camera):
    def __init__(self, *args, **kwargs):


        try:
            self.mypicamera = picamera.PiCamera()
            self.mypicamera.resolution = [320,240]
            self.mypicamera.start_preview()
            time.sleep(2)
            self.mypicamera.stop_preview()
            self.picamerastream = picamera.array.PiRGBArray(mypicamera) 
            #picamerawindow = cv2.namedWindow("picamera")
            self.enabled = True

        except Exception:
            self.enabled = False
    
    


    def TakePhoto(args):
        if args.enabled:
            
            args.mypicamera.capture(picamerastream, format='bgr', resize=(320,240))

            photo = MyPicamPhoto()
            photo.image = picamerastream.array
            #cv2.imshow("picamera", image)
            args.picamerastream.truncate(0)

            return photo
        else:
            return None
        

    def Close(args):
        if args.enabled:
            args.mypicamera.close()
            args.picamerastream.close()
            # cv2.namedWindow("picamera")

class MyPicamPhoto(Photo):
    pass