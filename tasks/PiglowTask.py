
from Task import Task
import time
class PiglowTask(Task):
    def onRun(args):

        print('Fading')
        args.Context.piglow.Fade()

        time.sleep(1)



       
   
   

              



