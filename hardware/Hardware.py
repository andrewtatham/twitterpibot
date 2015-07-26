

import subprocess

import platform




adresses = {"brightpi": 0x70, "piglow":0x54}


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
            
            
            # TODO
            self.piglowattached = False
            self.brightpiattached = True

            




