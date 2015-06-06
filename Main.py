


import logging


import Tkinter
from Tasks import Tasks


logging.basicConfig(filename='twitter.log',level=logging.INFO)



andrewpi = "andrewtathampi" 
andrewpiid = "2935295111"

andrew = "andrewtatham"
andrewid = "19201332"

helen = "morris_helen"
markr = "fuuuunnnkkytree"
jamie = "jami3rez"
dean = "dcspamoni"
chriswatson = "watdoghotdog"
fletch = "paulfletcher79"
simon = "Tolle_Lege"

users = [andrew, markr, jamie, helen, dean, chriswatson, simon]








top = Tkinter.Tk()

tasks = Tasks()

tasks.Init()

tasks.Start()


top.mainloop()


tasks.Stop();

print("Done")


















