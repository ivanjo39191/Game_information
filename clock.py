import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)


    print('do crawler')
    os.system("python crawler1.py")

sched.start()