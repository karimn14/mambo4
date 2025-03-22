import datetime
from gluon import current

def update_pengajuan_paket():
    db = current.db
    today = datetime.date.today()
    
    # Only process if today is a weekday (Monday=0 ... Friday=4)
    if today.weekday() >= 5:
        return f"Today {today} is weekend; no insertion performed."
    
    messages = []
    
    # Select active kontrak records for today
    rows = db((db.t_kontrak_disdik.tanggal_mulai <= today) & 
              (db.t_kontrak_disdik.tanggal_selesai >= today)).select()

    if not rows:
        return f"No active kontrak records found for {today}."

    for kontrak in rows:
        # Check if an entry for this combination already exists today.
        existing = db(
            (db.t_pengajuan_paket.id_vendor == kontrak.id_vendor) &
            (db.t_pengajuan_paket.jenis_paket == kontrak.jenis_paket) &
            (db.t_pengajuan_paket.time_stamp.year() == today.year) &
            (db.t_pengajuan_paket.time_stamp.month() == today.month) &
            (db.t_pengajuan_paket.time_stamp.day() == today.day)
        ).select().first()

        if not existing:
            # Debugging: Log the values of id_sekolah and id_paket
            print(f"Debug: id_sekolah={getattr(kontrak, 'id_sekolah', None)}, id_paket={kontrak.id_paket}")

            pengajuan_paket_id = db.t_pengajuan_paket.insert(
                id_vendor = kontrak.id_vendor,
                id_disdik = kontrak.id_disdik if hasattr(kontrak, 'id_disdik') else None,
                id_sekolah = kontrak.id_sekolah if hasattr(kontrak, 'id_sekolah') else None,
                id_paket = kontrak.id_paket,  # Adjust mapping as needed
                jumlah = kontrak.jumlah_paket_per_hari,
                jenis_paket = kontrak.jenis_paket,
                approve = False,
                time_stamp_setuju = None,
                time_stamp = datetime.datetime.now(),
                deleted = False
            )
            db.t_status_paket.insert(
                id_pengajuan_paket = pengajuan_paket_id,
                id_vendor = kontrak.id_vendor,
                id_disdik = kontrak.id_disdik if hasattr(kontrak, 'id_disdik') else None,
                id_sekolah = kontrak.id_sekolah if hasattr(kontrak, 'id_sekolah') else None,
                id_paket = kontrak.id_paket,  # Adjust mapping as needed
                status = "Pending",
                time_stamp = datetime.datetime.now(),
                deleted = False
            )
            messages.append(f"Inserted record for vendor {kontrak.id_vendor} with jenis_paket {kontrak.jenis_paket}.")
        else:
            messages.append(f"Record for vendor {kontrak.id_vendor} and jenis_paket {kontrak.jenis_paket} already exists for today.")
    
    db.commit()
    return "\n".join(messages)
