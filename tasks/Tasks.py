import threading
from StreamTweetsTask import StreamTweetsTask

from Queue import Queue
from ProcessInboxTask import ProcessInboxTask
from Context import Context
import logging
from pprint import pprint
from MonitorTask import MonitorTask
import time


class Tasks(object):
    
    def __init__(self, *args, **kwargs):

        self.taskList = [StreamTweetsTask(),
                         ProcessInboxTask(),
                         MonitorTask()]


        self.running = False

        context = Context()
        for task in self.taskList:
            task.Context = context

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
                task.onRun()
            except Exception as e:
                logging.exception(e.message, e.args)             
                print(e.message)
                #time.sleep(5)

    def Stop(args):

        args.running = False
        for thread in args.runThreads:
            thread.join() 

        stopThreads = map(lambda task : threading.Thread(target=task.onStop), args.taskList)

        for thread in stopThreads:
            thread.start()

        for thread in stopThreads:
            thread.join()


