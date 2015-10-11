import os
import pickle
import sys
import platform
import colorama
import datetime
try:
    from Tkinter import * 
except ImportError:
    from tkinter import * 

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

from Authenticator import Authenticator
from Context import Context
from Tasks import Tasks
from Schedule import Schedule
from OutgoingDirectMessage import OutgoingDirectMessage

if platform.node() != "ANDREWDESKTOP":
    colorama.init(autoreset = True)

auth = Authenticator()
auth.Authenticate()

context = Context()

tasks = Tasks(context=context)
tasks.Init()
tasks.Start()

scheduler = Schedule(context=context)
context.scheduler = scheduler
scheduler.Start()

if not context.hardware.iswindows:
    context.send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Up...." + str(datetime.datetime.now())))


top = Tk()
context.top = top

top.mainloop()

if not context.hardware.iswindows:
    context.send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Down...." + str(datetime.datetime.now())))

tasks.Stop()
scheduler.Stop()
#context.Stop()
print("Done")
sys.exit(0)
print("Exited")