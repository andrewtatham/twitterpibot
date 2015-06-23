import sys
sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')



import logging
import Tkinter
from Schedule import Schedule
from Context import Context
from Tasks import Tasks

logging.basicConfig(filename='twitter.log',level=logging.INFO)


top = Tkinter.Tk()

context = Context()

tasks = Tasks(context=context)

tasks.Init()

#schedule = Schedule(context=context)

#schedule.Start()

tasks.Start()

top.mainloop()

tasks.Stop();

#schedule.Stop()

print("Done")


















