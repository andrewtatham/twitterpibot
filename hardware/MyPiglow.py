import math
import time
import random
try:    
    from piglow import PiGlow
    #from PyGlow import PyGlow
    enablePiglow = True
except Exception as e:
    print(e)
    enablePiglow = False


class MyPiglow(object):
    def __init__(self, *args, **kwargs):

        self.t = 0;

        self.piglow = None
        if enablePiglow:
            self.piglow = PiGlow()
            #self.piglow = PyGlow()
            self.maxbright = 255
            self.piglow.all(0)


            #print('piglow init buffer')
            self.buffer = [0 for led in range(18)]

            self.InitPatterns()


        return super(MyPiglow, self).__init__(*args, **kwargs)

    def getLed(args, arm, colour):
        return int(6 * arm + colour)
    def getBright(args, factor):
        return max(0, min(int(-0.5 * args.maxbright + args.maxbright * factor),255))



    def InitPatterns(args):
        args.tweetMentionPattern = [[0 for x in range(360)]for y in range(18)]
        args.directMessagePattern = [[0 for x in range(360)]for y in range(18)]


        for t in range(360):
            for colour in range(6):
                for arm in range(3):

                    led = args.getLed(arm,colour)

                    b1 = math.sin(math.radians(t + arm * 15 + colour * 30))
                    args.tweetMentionPattern[led][t] = args.getBright(b1)

                    b2 = math.sin(math.radians(t - arm * 30 - colour * 15))
                    args.directMessagePattern[led][t] = args.getBright(b2)

    def DisplayPattern(args, pattern):
        if enablePiglow:
            for t in range(0, 360):               
                for led in range(18):
                    args.piglow.led(led + 1, pattern[led][args.t])
                time.sleep(0.05) 


    def OnInboxItemRecieved(args, inboxItem):
        if enablePiglow:
            if inboxItem.isTweet:
                if not inboxItem.from_me and inboxItem.to_me:
                    #args.DisplayPattern(args.tweetMentionPattern)
                    pass
                else:
                    led = random.randint(0,17)
                    args.buffer[led] = max(0, min((args.buffer[led] + 1), 255))
                    args.WriteLed(led)
            elif inboxItem.isDirectMessage:
                if not inboxItem.from_me and inboxItem.to_me:
                    #args.DisplayPattern(args.directMessagePattern)
                    pass



    def Fade(args):
        if enablePiglow:
            for led in range(18):
                if args.buffer[led] > 1:
                    args.buffer[led] = max(0,args.buffer[led] - 5)        
            args.WriteAll()

    def WriteAll(args):
        if enablePiglow:
            for led in range(18):
                args.WriteLed(led)
                

    def WriteLed(args, led):
        if enablePiglow:
            bright = max(0, min(args.buffer[led], 255))
            args.piglow.led(led + 1, bright)

    def CameraFlash(args, on):
        if enablePiglow:
            if on:
                args.piglow.white(255)
            else:
                args.WriteAll()