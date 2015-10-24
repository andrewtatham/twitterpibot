import sys
import time
import MyLogging
import logging
logger = logging.getLogger(__name__)



import hardware
import Identity
import TwitterHelper
TwitterHelper.Init(Identity.screen_name)
import colorama

if not hardware.isAndrewDesktop:
    colorama.init(autoreset = True)

import Tasks
Tasks.Start()
time.sleep(1)

import MySchedule
MySchedule.Start()
time.sleep(1)

import datetime
from TwitterHelper import Send
from OutgoingDirectMessage import OutgoingDirectMessage
#if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        screen_name = "andrewtatham", 
#        user_id = "19201332", 
#        text="Up...." + str(datetime.datetime.now())))
#    time.sleep(1)

import MyUI
MyUI.Start()


#if not hardware.iswindows:
#    Send(OutgoingDirectMessage(
#        screen_name = "andrewtatham", 
#        user_id = "19201332", 
#        text="Down...." + str(datetime.datetime.now())))

Tasks.Stop()
MySchedule.Stop()
hardware.Stop()
print("Done")
sys.exit(0)
