import sys
sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')




import Tkinter
from Schedule import Schedule
from Context import Context
from Tasks import Tasks

import colorama



colorama.init()


context = Context()

tasks = Tasks(context=context)
tasks.Init()
tasks.Start()

schedule = Schedule(context=context)
schedule.Start()

top = Tkinter.Tk()
top.mainloop()


print("Exiting...")
tasks.Stop();
schedule.Stop()
print("Done")


















