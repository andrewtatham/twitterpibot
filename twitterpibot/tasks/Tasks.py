import threading
from multiprocessing import Lock
import logging

from twitterpibot.ExceptionHandler import handle

logger = logging.getLogger(__name__)

_global_running = False
_task_running = {}
_task_dic = {}
_lock = Lock()


def start():
    global _global_running
    _global_running = True
    import twitterpibot.Identity as Identity
    tasks = Identity.get_tasks()
    for task in tasks:
        add(task)


def add(task):
    runthread = threading.Thread(target=_run_wrapper, args=[task], name=task.key)
    _task_dic[task.key] = (task, runthread)
    _task_running[task.key] = True
    logger.debug("[Tasks] starting thread %s", task.key)
    runthread.start()


def _run_wrapper(task):
    while _global_running and (task.core or _task_running[task.key]):
        try:
            task.onRun()
        except Exception as e:
            logger.debug("[Tasks] exception in thread %s", task.key)
            handle(e)
    logger.debug("[Tasks] exiting thread %s", task.key)


def get():
    return [k for k, v in _task_dic.items() if not v[0].core]


def remove(key):
    task = _task_dic[key][0]
    runthread = _task_dic[key][1]
    if _task_running[key]:
        logger.debug("[Tasks] stopping thread %s", key)
        _task_running[key] = False
        task.onStop()
        runthread.join()
        logger.debug("[Tasks] stopped thread %s", key)


def stop():
    logger.info("Stopping")

    global _global_running
    _global_running = False

    for task in _task_dic.keys():
        remove(task)

    logger.info("Stopped")