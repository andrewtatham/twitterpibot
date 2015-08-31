import ptvsd
import os
import pickle
import sys
import platform
import colorama
import Tkinter

from Context import Context
from Tasks import Tasks
from Schedule import Schedule

sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')
sys.path.append('users')

sys.path.append('brightpi')

if platform.node() <> "ANDREWDESKTOP":
    colorama.init()

context = Context()

tasks = Tasks(context=context)
tasks.Init()
tasks.Start()

scheduler = Schedule(context=context)
context.scheduler = scheduler
scheduler.Start()

top = Tkinter.Tk()
top.mainloop()

print("Exiting...")
tasks.Stop()
scheduler.Stop()
#context.Stop()
print("Done")
sys.exit(0)