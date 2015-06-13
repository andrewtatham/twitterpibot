import math
import time
try:    
    from piglow import PiGlow
except Exception:
    enablePiglow = False


class MyPiglow(object):
    def __init__(self, *args, **kwargs):

        self.t = 0;

        self.piglow = None
        if enablePiglow:
            self.piglow = PiGlow()
            self.maxbright = 32
            self.piglow.all(0)
            self.pattern = [[0 for x in range(360)]for y in range(18)]
            for t in range(360):
                for colour in range(6):
                    for arm in range(3):
                        b1 = math.sin(math.radians(t + arm * 15 + colour * 360 / 32))
                        led = self.getLed(arm,colour)
                        self.pattern[led][t] = self.getBright(b1)

        return super(MyPiglow, self).__init__(*args, **kwargs)

    def getLed(args, arm,colour):
        return int(6 * arm + colour)
    def getBright(args, factor):
        return max(0, min(int(-0.5 * args.maxbright + args.maxbright * factor),255))

    def Display(args):

        if enablePiglow:
            if args.t >= 360:
                args.t = 0
            else:
                args.t += 1




            for led in range(18):
                args.piglow.led(led + 1, args.pattern[led][args.t])
             
            time.sleep(1) 
       


