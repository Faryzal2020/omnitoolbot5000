from apscheduler.schedulers.blocking import BlockingScheduler

from reminder import Reminder

sched = BlockingScheduler()
rem = Reminder()

@sched.scheduled_job('interval', seconds=15)
def timed_job():
	rem.checkExpiry()

sched.start()