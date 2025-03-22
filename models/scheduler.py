from scheduler_tasks import update_pengajuan_paket
from gluon.scheduler import Scheduler

scheduler = Scheduler(db, dict(
    update_pengajuan_paket=update_pengajuan_paket
))

# Queue the task with a period of 60 seconds (or your desired interval)
scheduler.queue_task('update_pengajuan_paket', period=1000)
