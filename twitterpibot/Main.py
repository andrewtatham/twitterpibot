import sys
import time
import logging
import twitterpibot.hardware.hardware as hardware
import twitterpibot.Identity as Identity
import twitterpibot.twitter.TwitterHelper as TwitterHelper
import colorama
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI

logger = logging.getLogger(__name__)

TwitterHelper.Init(Identity.screen_name)

if not hardware.isAndrewDesktop:
    colorama.init(autoreset=True)

Tasks.Start()
time.sleep(1)

MySchedule.Start()
time.sleep(1)

# if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        screen_name = "andrewtatham", 
#        user_id = "19201332", 
#        text="Up...." + str(datetime.datetime.now())))
#    time.sleep(1)


MyUI.Start()


# if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        screen_name = "andrewtatham", 
#        user_id = "19201332", 
#        text="Down...." + str(datetime.datetime.now())))

Tasks.Stop()
MySchedule.Stop()
hardware.Stop()
print("Done")
sys.exit(0)
