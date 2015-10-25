import sys
import logging

import colorama

import twitterpibot.hardware.hardware as hardware
import twitterpibot.Identity as Identity
import twitterpibot.twitter.TwitterHelper as TwitterHelper
import twitterpibot.tasks.Tasks as Tasks
import twitterpibot.schedule.MySchedule as MySchedule
import twitterpibot.MyUI as MyUI

logger = logging.getLogger(__name__)

TwitterHelper.init(Identity.screen_name)

if not hardware.is_andrew_desktop:
    colorama.init(autoreset=True)

Tasks.start()

MySchedule.start()

# if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        text="Up...." + str(datetime.datetime.now())))

MyUI.start()

# if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        text="Down...." + str(datetime.datetime.now())))

Tasks.stop()
MySchedule.stop()
hardware.Stop()
print("Done")
sys.exit(0)
