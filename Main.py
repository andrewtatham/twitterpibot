import sys
import time

sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')
sys.path.append('users')
sys.path.append('processing')
sys.path.append('brightpi')
sys.path.append('songs')
#sys.path.append('PiGlow')
sys.path.append('PyGlow')

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
if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Up...." + str(datetime.datetime.now())))
    time.sleep(1)

import MyUI
MyUI.Start()


if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Down...." + str(datetime.datetime.now())))

Tasks.Stop()
MySchedule.Stop()
hardware.Stop()
print("Done")
sys.exit(0)
print("Exited")