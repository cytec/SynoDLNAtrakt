from lib.apscheduler.scheduler import Scheduler

sched = Scheduler()
sched.configure({'apscheduler.misfire_grace_time':10})