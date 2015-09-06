import subprocess
import platform

class Hardware(object):
    def __init__(self, *args, **kwargs):

        pl = platform.platform()

        self.iswindows = pl.startswith('Windows')

        if self.iswindows:
            self.piglowattached = False
            self.brightpiattached = False

        else:
            test = subprocess.Popen(["sudo","i2cdetect","-y","1"], stdout=subprocess.PIPE)
            output = test.communicate()[0]
            print(str(output))
            
            self.piglowattached = True # bool(" 54 " in output)
            self.brightpiattached = bool(" 70 " in output)

            if self.piglowattached:
                print ("Detected 54 PiGlow")
            if self.brightpiattached:
                print ("Detected 70 BrightPi")