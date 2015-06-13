try:
    import picamera
    import picamera.array
except Exception:
    enablePicam = False


def PicameraTasks(args):
    mypicamera = None
    picamerastream = None
    picamerawindow = None
    if enablePicam:
        mypicamera = picamera.PiCamera()
        mypicamera.resolution = [320,240]
        mypicamera.start_preview()
        time.sleep(2)
        mypicamera.stop_preview()
        picamerastream = picamera.array.PiRGBArray(mypicamera) 
        picamerawindow = cv2.namedWindow("picamera")

        while running and enablePicam:
            try:
                mypicamera.capture(picamerastream, format='bgr', resize=(320,240))
                image = picamerastream.array
                cv2.imshow("picamera", image)
                picamerastream.truncate(0)
                #cv2.waitKey(1)
                time.sleep(5)

            except Exception as e:

                logging.exception(e.message, e.args)             
                pprint.pprint(e)

    def onStop(args):
        if enablePicam:
            mypicamera.close()
            picamerastream.close()
            cv2.namedWindow("picamera")
                
    def TakePhoto(args):
        path = "pics/pinoir.jpg"
        #mypicamera.start_preview()
        mypicamera.capture(path) 
        #mypicamera.stop_preview()
        return path