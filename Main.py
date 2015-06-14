


import logging


import Tkinter

import sys
from Schedule import Schedule

sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')

from Tasks import Tasks

logging.basicConfig(filename='twitter.log',level=logging.INFO)


top = Tkinter.Tk()

tasks = Tasks()

tasks.Init()

schedule = Schedule()

schedule.Start()
tasks.Start()

top.mainloop()


tasks.Stop();
schedule.Stop()

print("Done")


















