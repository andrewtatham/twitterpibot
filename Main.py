import sys
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

import colorama


import datetime








from Authenticator import Authenticator
auth = Authenticator()
auth.Authenticate()

import hardware
if not hardware.isAndrewDesktop:
    colorama.init(autoreset = True)




from Tasks import Tasks

tasks = Tasks()
tasks.Init()
tasks.Start()

import MySchedule
MySchedule.Start()


from OutgoingDirectMessage import OutgoingDirectMessage


if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Up...." + str(datetime.datetime.now())))


try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk

top = Tk()
top.mainloop()

if not hardware.iswindows:
    Send(OutgoingDirectMessage(
        screen_name = "andrewtatham", 
        user_id = "19201332", 
        text="Down...." + str(datetime.datetime.now())))

tasks.Stop()
MySchedule.Stop()
hardware.Stop()
print("Done")
sys.exit(0)
print("Exited")