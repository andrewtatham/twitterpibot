
from Task import Task
import time


class SongTask(Task):
    def onRun(args):
    

        tweet = args.Context.song.get()            
        args.Context.outbox.put(tweet)
        args.Context.song.task_done()
        time.sleep(5)



