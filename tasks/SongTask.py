
from Task import Task
import time


class SongTask(Task):
    def onRun(args):
    
        try:
            tweet = args.context.song.get()            
            args.context.outbox.put(tweet)
        finally:
            args.context.song.task_done()
            time.sleep(5)



