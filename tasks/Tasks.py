import threading
from StreamTweetsTask import StreamTweetsTask
from ProcessInboxTask import ProcessInboxTask

from PiglowTask import PiglowTask
from ExceptionHandler import Handle
from exceptions import Exception

global hardware

class Tasks(object):
    
    def __init__(self, *args, **kwargs):

        self.taskList = [ProcessInboxTask(),
                         StreamTweetsTask()]
        if hardware.piglowattached:
            self.taskList.append(PiglowTask())

        self.running = False


    def Init(args):

        initThreads = []
        for task in args.taskList:
            initThreads.append(threading.Thread(target=task.onInit))

        for thread in initThreads:
            thread.start()

        for thread in initThreads:
            thread.join()



    def Start(args):

        args.running = True

        args.runThreads = []
        for task in args.taskList:

            runThread = threading.Thread(target=args.RunWrapper, args=[task])
            #runThread.setDaemon(True)
            args.runThreads.append(runThread)

        for thread in args.runThreads:
            thread.start()

    def RunWrapper(args, task):
        while args.running:           
            try:   
                if task.enabled:
                    task.onRun()
            except Exception as e:                
                Handle(e)

    def Stop(args):
        args.running = False
       
        stopThreads = map(lambda task : threading.Thread(target=task.onStop), args.taskList)
        for thread in stopThreads:
            thread.start()
        for thread in stopThreads:
            thread.join()
        for thread in args.runThreads:
            thread.join()
