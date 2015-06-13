
from Camera import Camera, Photo
import time


try:
    import picamera
    import picamera.array

except Exception as e:
    print(e.message)
  


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

        except Exception as e:
            print(e.message)
            self.enabled = False
                
    
    


    def TakePhoto(args):
        if args.enabled:
            print('taking photo')
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