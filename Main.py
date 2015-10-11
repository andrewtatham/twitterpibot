import sys

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

import os
import pickle
import platform
import colorama
import Tkinter
import datetime
from multiprocessing import Queue

from Authenticator import Authenticator
from Hardware import Hardware
from Cameras import Cameras
from Users import Users
from Tasks import Tasks
from Schedule import Schedule
from OutgoingDirectMessage import OutgoingDirectMessage
from MyPiglow import MyPiglow
from MyBrightPi import MyBrightPi

if platform.node() != "ANDREWDESKTOP":
    colorama.init(autoreset = True)

auth = Authenticator()
auth.Authenticate()


inbox = Queue()
users = Users()
piglow = None
brightpi = None
hardware = Hardware()
cameras = Cameras()
if hardware.piglowattached:
    piglow = MyPiglow()
if hardware.brightpiattached:
    brightpi = MyBrightPi()

tasks = Tasks()
tasks.Init()
tasks.Start()

scheduler = Schedule()
scheduler = scheduler
scheduler.Start()

if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Up...." + str(datetime.datetime.now())))


top = Tkinter.Tk()
top = top

top.mainloop()

if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Down...." + str(datetime.datetime.now())))

tasks.Stop()
scheduler.Stop()
print("Done")
sys.exit(0)
print("Exited")