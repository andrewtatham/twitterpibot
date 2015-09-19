
from Task import Task
import time
import sys


class SongTask(Task):
    def onRun(args):
    
        try:
            tweet = args.context.song.get()   
            if tweet:      
                args.context.outbox.put(tweet)
        finally:
            args.context.song.task_done()
            time.sleep(5)

    def onStop(args):
        args.context.song.put(None)


