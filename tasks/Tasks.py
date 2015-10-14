import threading
from ExceptionHandler import Handle
import Identity

_taskList = Identity.GetTasks()
_running = False
_runThreads = []


def Start():
    global _running
    _running = True

    global _taskList
    global _runThreads
    for task in _taskList:

        runThread = threading.Thread(target=RunWrapper, args=[task])
        _runThreads.append(runThread)

    for thread in _runThreads:
        thread.start()

def RunWrapper(task):
    global _running
    while _running:           
        try:   
            task.onRun()
        except Exception as e:                
            Handle(e)

def Stop():
    global _running
    _running = False
       
    global _taskList
    global _runThreads
    stopThreads = map(lambda task : threading.Thread(target=task.onStop), _taskList)
    for thread in stopThreads:
        thread.start()
    for thread in stopThreads:
        thread.join()
    for thread in _runThreads:
        thread.join()
