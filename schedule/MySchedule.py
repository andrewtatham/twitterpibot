

from ExceptionHandler import Handle
import Identity
from apscheduler.schedulers.background import BackgroundScheduler




def RunWrapper(task):
    try:   
        task.onRun()
    except Exception as e:
        Handle(e)

def Start():
    _scheduler.start()
def Stop():
    _scheduler.shutdown()
    for job in _jobs:
        job.onStop()

def add(job):
    _scheduler.add_job(RunWrapper, args=[job], trigger = job.GetTrigger())




_scheduler = BackgroundScheduler()
_jobs = Identity.GetScheduledJobs()

for job in _jobs:
    _scheduler.add_job(RunWrapper, args=[job], trigger = job.GetTrigger())



