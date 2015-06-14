
from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler



class Schedule(object):
    def __init__(self, *args, **kwargs):

        self.scheduler = BackgroundScheduler()

    
        self.scheduler.add_job(self.tick, 'interval', seconds=3)
        self.scheduler.add_job(self.tock, 'interval', seconds=7)
      
        # Schedules job_function to be run on the third Friday
        # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
        sched.add_cron_job(job_function, month='6-8,11-12', day='3rd fri', hour='0-3')

        # Initialization similar as above, the backup function defined elsewhere

        # Schedule a backup to run once from Monday to Friday at 5:30 (am)
        sched.add_cron_job(backup, day_of_week='mon-fri', hour=5, minute=30)

        # birthdays
        # me 2nd jan
        #helen 20th may

        # jamie#
        # mark r

        # christmas
        # new year




        # TODO

        # sept 19th talk like a pirate day

        # "@edballs ED BALLS #EdBallsDay" "28th April 4:20 pm"


        return super(Schedule, self).__init__(*args, **kwargs)



    def tick(args):
        print('Tick')    
    def tock(args):
        print('Tock')


    def Start(args):
        args.scheduler.start()
    def Stop(args):
        args.scheduler.shutdown() 
        
