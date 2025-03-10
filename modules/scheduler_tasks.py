
import datetime
from gluon import current

def update_pengajuan_paket():
    """
    Fungsi ini dijalankan setiap hari untuk memproses kontrak aktif dan menginsert data
    ke tabel t_pengajuan_paket sesuai dengan logika bisnis.
    """
    today = datetime.date.today()
    db = current.db

    # Contoh logika: hanya proses jika hari ini Senin-Jumat
    if today.weekday() > 6:
        return f"Hari ini bukan hari kerja: {today.strftime('%Y-%m-%d')}"
    
    # Misal, ambil semua data kontrak aktif
    rows = db(db.t_kontrak_disdik.tanggal_mulai <= today)\
           (db.t_kontrak_disdik.tanggal_selesai >= today).select()
    
    for kontrak in rows:
        # Cek duplikasi berdasarkan kombinasi id_vendor, jenis_paket, dan tanggal task
        existing = db(
            (db.t_pengajuan_paket.id_vendor == kontrak.id_vendor) &
            (db.t_pengajuan_paket.jenis_paket == kontrak.jenis_paket) &
            (db.t_pengajuan_paket.time_stamp.year() == today.year) &
            (db.t_pengajuan_paket.time_stamp.month() == today.month) &
            (db.t_pengajuan_paket.time_stamp.day() == today.day)
        ).select().first()
        
        if not existing:
            db.t_pengajuan_paket.insert(
                id_paket = None,  # Atur logika mapping id paket sesuai kebutuhan
                jumlah = kontrak.jumlah_paket_per_hari,
                approve = False,
                id_pengaju = kontrak.id_disdik if hasattr(kontrak, 'id_disdik') else None,
                id_approver = None,
                time_stamp_setuju = None,
                id_vendor = kontrak.id_vendor,
                jenis_paket = kontrak.jenis_paket,
                time_stamp = datetime.datetime.now(),
                deleted = False
            )
    db.commit()
    return f"Task update_pengajuan_paket dijalankan pada {today.strftime('%Y-%m-%d')}"
