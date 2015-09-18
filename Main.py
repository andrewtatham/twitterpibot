import os
import pickle
import sys
import platform
import colorama
import Tkinter
import datetime

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

context.outbox.put(OutgoingDirectMessage(
    screen_name = "andrewtatham", 
    user_id = "19201332", 
    text="Up...." + str(datetime.datetime.now())))


top = Tkinter.Tk()
top.mainloop()

print("Exiting...")
tasks.Stop()
scheduler.Stop()
#context.Stop()
print("Done")
sys.exit(0)