import ptvsd
import os
import pickle


## TODO Encrypt
#filename = 'REMOTE_DEBUG.PKL'
#if os.path.isfile(filename):
#    pw = pickle.load(open(filename, "rb"))

#else:
#    pw = raw_input('Enter a password to eable remote debugging, or press enter
#    to skip:')
#    if pw and pw <> '':
#        pickle.dump(pw, open(filename, "wb"))

#if pw and pw <> '':
#    ptvsd.enable_attach(pw)
import sys
sys.path.append('tasks')
sys.path.append('incoming')
sys.path.append('responses')
sys.path.append('outgoing')
sys.path.append('hardware')
sys.path.append('twitter')
sys.path.append('schedule')
sys.path.append('users')

sys.path.append('brightpi')

import platform


import colorama
if platform.node() <> "ANDREWDESKTOP":
    colorama.init()


from Context import Context
context = Context()

from Tasks import Tasks
tasks = Tasks(context=context)
tasks.Init()
tasks.Start()

from Schedule import Schedule
scheduler = Schedule(context=context)
context.scheduler = scheduler
scheduler.Start()

import Tkinter
top = Tkinter.Tk()
top.mainloop()

print("Exiting...")
tasks.Stop()
scheduler.Stop()
context.Stop()
print("Done")


















