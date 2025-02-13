@request.restful()
@cors_allow
def paket_sekolah_kepsek():
    response.view = 'generic.json'

    # 📌 URI: GET /paket_sekolah_kepsek/list
    def GET():
        """ Mengambil daftar paket berdasarkan sekolah kepala sekolah yang sedang login """
        sekolahan_saya = db(
            (db.map_sekolah_kepala.id_kepala_sekolah == auth.user.id) &  
            (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id)
        ).select().as_list()

        daftar_paket = []
        nama_sekolah = ""

        if len(sekolahan_saya) == 1:
            id_sekolah = sekolahan_saya[0]['m_sekolah']['id']
            nama_sekolah = sekolahan_saya[0]['m_sekolah']['nama_sekolah']

            daftar_paket = db(
                (db.t_pemberian_paket.id_paket == db.m_paket.id) &
                (db.t_pemberian_paket.id_tujuan == id_sekolah) &
                (db.t_pemberian_paket.tanggal_pengiriman_dari_vendor != None) &
                (db.t_pemberian_paket.deleted == False)
            ).select().as_list()

        return dict(paket=daftar_paket, nama_sekolah=nama_sekolah)

    # 📌 URI: POST /paket_sekolah_kepsek/add
    def POST():
        """ Menambahkan data baru ke t_tanda_terima_paket """
        try:
            data = json.loads(request.body.read())
            if not isinstance(data, list):
                return dict(status="error", message="Data harus berupa list")

            inserted_records = []
            for entry in data:
                id_paket = entry.get("id_paket")
                jumlah_terima = entry.get("jumlah_dari_vendor")
                tanggal_terima = entry.get("tanggal_pengiriman_dari_vendor")

                if not jumlah_terima or not tanggal_terima:
                    return dict(status="error", message="Field jumlah dan tanggal_terima harus diisi")

                new_id = db.t_tanda_terima_paket.insert(
                    id_t_pemberian_paket=id_paket,
                    jumlah=jumlah_terima,
                    tanggal_terima=tanggal_terima,
                    id_user=auth.user.id,
                    time_stamp=request.now
                )
                inserted_records.append(new_id)

            db.commit()
            return dict(status="success", message="Data berhasil ditambahkan", inserted_ids=inserted_records)

        except Exception as e:
            return dict(status="error", message=str(e))

    # 📌 URI: PUT /paket_sekolah_kepsek/update
    def PUT():
        """ Memperbarui data t_pemberian_paket berdasarkan id_paket """
        try:
            data = json.loads(request.body.read())
            if not isinstance(data, list):
                return dict(status="error", message="Data harus berupa list")

            updated_records = []
            for entry in data:
                id_paket = entry.get("id_paket")
                jumlah_terima = entry.get("jumlah_dari_vendor")
                tanggal_terima = entry.get("tanggal_pengiriman_dari_vendor")

                if not jumlah_terima or not tanggal_terima:
                    return dict(status="error", message="Field jumlah dan tanggal_terima harus diisi")

                paket = db(db.t_pemberian_paket.id == id_paket).select().first()
                if not paket:
                    return dict(status="error", message="Paket tidak ditemukan")

                paket.update_record(
                    tanggal_pengiriman_dari_vendor=tanggal_terima,
                    jumlah_dari_vendor=jumlah_terima
                )
                updated_records.append(id_paket)

            db.commit()
            return dict(status="success", message="Data berhasil diperbarui", updated_ids=updated_records)

        except Exception as e:
            return dict(status="error", message=str(e))

    # 📌 URI: DELETE /paket_sekolah_kepsek/delete/{id_paket}
    def DELETE(id_paket):
        """ Menghapus data di t_pemberian_paket berdasarkan ID """
        try:
            if not id_paket:
                return dict(status="error", message="ID paket harus diberikan")

            paket = db(db.t_pemberian_paket.id == id_paket).select().first()
            if not paket:
                return dict(status="error", message="Paket tidak ditemukan")

            # Pilihan: Soft delete atau Hard delete
            db(db.t_pemberian_paket.id == id_paket).delete()
            db.commit()

            return dict(status="success", message=f"Paket dengan ID {id_paket} berhasil dihapus")

        except Exception as e:
            return dict(status="error", message=str(e))

    return locals()
