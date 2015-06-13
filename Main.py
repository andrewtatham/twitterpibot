


import logging


import Tkinter

import sys

sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')

from Tasks import Tasks

logging.basicConfig(filename='twitter.log',level=logging.INFO)


top = Tkinter.Tk()

tasks = Tasks()

tasks.Init()

tasks.Start()


top.mainloop()


tasks.Stop();

print("Done")


















