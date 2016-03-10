import threading
import logging
import time
from twitterpibot.exceptionmanager import handle

logger = logging.getLogger(__name__)

_global_running = False
_task_running = {}
_task_dic = {}
_tasks = []


def start():
    global _global_running
    _global_running = True
    for task in _tasks:
        time.sleep(1)
        add(task)


def add(task):
    runthread = threading.Thread(target=_run_wrapper, args=[task], name=task.key)
    _task_dic[task.key] = (task, runthread)
    _task_running[task.key] = True
    logger.info("[Tasks] starting thread %s", task.key)
    runthread.start()


def _run_wrapper(task):
    while _global_running and (task.core or bool(_task_running[task.key])):
        try:
            task.on_run()
        except Exception as e:
            logger.warn("[Tasks] exception in thread %s", task.key)
            handle(task.identity, e)
    logger.info("[Tasks] exiting thread %s", task.key)


def get_all():
    return _task_dic.keys()


def get():
    return [k for k, v in _task_dic.items() if not v[0].core and bool(_task_running[v[0].key])]


def remove(key):
    task = _task_dic[key][0]
    runthread = _task_dic[key][1]
    if _task_running[key]:
        logger.info("[Tasks] stopping thread %s", key)
        _task_running[key] = False
        task.on_stop()
        runthread.join()
        logger.info("[Tasks] stopped thread %s", key)


def stop():
    logger.info("Stopping")

    global _global_running
    _global_running = False

    for task in _task_dic.keys():
        remove(task)

    logger.info("Stopped")


def set_tasks(identities):
    global _tasks
    _tasks = []
    for identity in identities:
        _tasks.extend(identity.get_tasks())
