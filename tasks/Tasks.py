import threading
from StreamTweetsTask import StreamTweetsTask

from Queue import Queue
from ProcessInboxTask import ProcessInboxTask
from Context import Context
import logging
from pprint import pprint
import time
from ProcessOutboxTask import ProcessOutboxTask
from SongTask import SongTask
from PiglowTask import PiglowTask
from ExceptionHandler import ExceptionHandler


class Tasks(object):
    
    def __init__(self, context, *args, **kwargs):

        self.taskList = [SongTask(),
                         ProcessOutboxTask(),
                         ProcessInboxTask(),
                         StreamTweetsTask()]
        
        if context.piglow:
            self.taskList.append(PiglowTask())


        self.running = False

        for task in self.taskList:
            task.context = context

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
                ExceptionHandler().Handle(e)
                #time.sleep(5)

    def Stop(args):

        args.running = False



        stopThreads = map(lambda task : threading.Thread(target=task.onStop), args.taskList)

        #print("stopping")
        for thread in stopThreads:
            #print(".")
            thread.start()

        #print("wait 1")
        for thread in stopThreads:
            #print(".")
            thread.join()

        #print("wait 2")
        #for thread in args.runThreads:
        #    print(".")
        #    thread.join() 
