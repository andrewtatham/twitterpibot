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



top = Tkinter.Tk()

context = Context()

tasks = Tasks(context=context)

tasks.Init()

schedule = Schedule(context=context)

schedule.Start()
tasks.Start()

top.mainloop()


print("Exiting...")
tasks.Stop();
schedule.Stop()
print("Done")


















