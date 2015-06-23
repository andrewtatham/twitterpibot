
from Task import Task
import time
class PiglowTask(Task):
    def onRun(args):

        #print('Fading')
        args.context.piglow.Fade()

        time.sleep(1)



       
   
   

              



