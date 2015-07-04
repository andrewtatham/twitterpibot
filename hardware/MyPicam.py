
from Camera import Camera, Photo
import time
from ExceptionHandler import ExceptionHandler


try:
    import picamera
    import picamera.array

except Exception as e:
    ExceptionHandler().HandleSilently(e)

  


class MyPicam(Camera):
    def __init__(self, *args, **kwargs):


        try:
            self.mypicamera = picamera.PiCamera()
            self.mypicamera.resolution = (640,480)
            #self.mypicamera.start_preview()
            #time.sleep(2)
            #self.mypicamera.stop_preview()
            self.picamerastream = picamera.array.PiRGBArray(self.mypicamera) 
            #picamerawindow = cv2.namedWindow("picamera")
            self.enabled = True

        except Exception as e:
            ExceptionHandler().HandleSilently(e)
            self.enabled = False
                
    
    


    def TakePhoto(args):
        if args.enabled:
            print('taking photo')
            args.mypicamera.capture(args.picamerastream, format='bgr')

            photo = MyPicamPhoto()
            photo.image = args.picamerastream.array
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