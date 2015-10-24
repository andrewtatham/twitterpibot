import threading
from twitterpibot.ExceptionHandler import Handle
import twitterpibot.Identity as Identity

_taskList = Identity.get_tasks()
_running = False
_runThreads = []


def start():
    global _running
    _running = True

    global _taskList
    global _runThreads
    for task in _taskList:
        runThread = threading.Thread(target=_run_wrapper, args=[task])
        _runThreads.append(runThread)

    for thread in _runThreads:
        thread.start()


def _run_wrapper(task):
    global _running
    while _running:
        try:
            task.onRun()
        except Exception as e:
            Handle(e)


def stop():
    global _running
    _running = False

    global _taskList
    global _runThreads
    stopThreads = map(lambda task: threading.Thread(target=task.onStop), _taskList)
    for thread in stopThreads:
        thread.start()
    for thread in stopThreads:
        thread.join()
    for thread in _runThreads:
        thread.join()
