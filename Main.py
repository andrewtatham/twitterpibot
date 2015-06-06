


import logging


import Tkinter
from Tasks import Tasks


logging.basicConfig(filename='twitter.log',level=logging.INFO)


top = Tkinter.Tk()

tasks = Tasks()

tasks.Init()

tasks.Start()


top.mainloop()


tasks.Stop();

print("Done")


















