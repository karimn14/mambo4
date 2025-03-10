# File: applications/mambo4/models/scheduler.py
from scheduler_tasks import update_pengajuan_paket
from gluon.scheduler import Scheduler

# Inisialisasi scheduler dengan daftar task
scheduler = Scheduler(db, dict(
    update_pengajuan_paket=update_pengajuan_paket
))

def task_in_queue(task_name):
    """
    Mengecek apakah ada task dengan nama `task_name` yang berstatus QUEUED atau RUNNING.
    """
    query = (db.scheduler_task.task_name == task_name) & \
            (db.scheduler_task.status.belongs(['QUEUED', 'RUNNING']))
    return db(query).count() > 0

# Cek jika task belum ada dalam antrian, maka queue task tersebut dengan interval 86400 detik (24 jam)
if not task_in_queue('update_pengajuan_paket'):
    scheduler.queue_task('update_pengajuan_paket', period=60)
