from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
from apscheduler.schedulers.base import STATE_RUNNING
from apscheduler.triggers.interval import IntervalTrigger
import time

def myfunc():
    print("Hello")


trigger = IntervalTrigger(seconds=10)
sched.add_job(myfunc, trigger)
sched.start()

time.sleep(15)

if(sched.state == STATE_RUNNING):
    sched.shutdown()
    print("SHut dOWn")

trigger = IntervalTrigger(seconds=10)
sched = BackgroundScheduler()
sched.add_job(myfunc, trigger)
sched.start()

time.sleep(15)
