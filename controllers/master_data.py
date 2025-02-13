
@auth.requires_membership('super_admin')
def master_supplier():
    q= ( (db.m_supplier.id_kelurahan_desa == db.m_kelurahan_desa.id)& 
         (db.m_kelurahan_desa.id_kecamatan == db.m_kecamatan.id)& 
         (db.m_kecamatan.id_kabupaten_kota == db.m_kabupaten_kota.id)& 
         (db.m_kabupaten_kota.id_propinsi == db.m_propinsi.id)
        )
    fields = (db.m_supplier.id, db.m_supplier.nama_supplier, db.m_supplier.alamat, 
        db.m_kelurahan_desa.kelurahan_desa, db.m_kecamatan.kecamatan,
        db.m_kabupaten_kota.kabupaten_kota, db.m_propinsi.propinsi
        )        
    grid = SQLFORM.grid(q, fields=fields, create=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_vendor():
    q= ( (db.m_vendor.id_kelurahan_desa == db.m_kelurahan_desa.id)& 
         (db.m_kelurahan_desa.id_kecamatan == db.m_kecamatan.id)& 
         (db.m_kecamatan.id_kabupaten_kota == db.m_kabupaten_kota.id)& 
         (db.m_kabupaten_kota.id_propinsi == db.m_propinsi.id)
        )
    fields = (db.m_vendor.id, db.m_vendor.nama_vendor, db.m_supplier.alamat, 
        db.m_kelurahan_desa.kelurahan_desa, db.m_kecamatan.kecamatan,
        db.m_kabupaten_kota.kabupaten_kota, db.m_propinsi.propinsi
        )        
    grid = SQLFORM.grid(q, fields=fields, searchable=True, editable=True, deletable=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_sekolah():
    q= ( (db.m_sekolah.id_kelurahan_desa == db.m_kelurahan_desa.id)& 
         (db.m_kelurahan_desa.id_kecamatan == db.m_kecamatan.id)& 
         (db.m_kecamatan.id_kabupaten_kota == db.m_kabupaten_kota.id)& 
         (db.m_kabupaten_kota.id_propinsi == db.m_propinsi.id)
        )
    fields = (db.m_sekolah.id, db.m_sekolah.nama_sekolah, db.m_sekolah.alamat, 
        db.m_kelurahan_desa.kelurahan_desa, db.m_kecamatan.kecamatan,
        db.m_kabupaten_kota.kabupaten_kota, db.m_propinsi.propinsi
        )
    grid = SQLFORM.grid(q, fields=fields
        , create=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_disdik():
    q= ( (db.m_disdik.id_kelurahan_desa == db.m_kelurahan_desa.id)& 
         (db.m_kelurahan_desa.id_kecamatan == db.m_kecamatan.id)& 
         (db.m_kecamatan.id_kabupaten_kota == db.m_kabupaten_kota.id)& 
         (db.m_kabupaten_kota.id_propinsi == db.m_propinsi.id)
        )
    fields = (db.m_disdik.id, db.m_disdik.nama_disdik, db.m_disdik.alamat, 
        db.m_kelurahan_desa.kelurahan_desa, db.m_kecamatan.kecamatan,
        db.m_kabupaten_kota.kabupaten_kota, db.m_propinsi.propinsi
        )    
    grid = SQLFORM.grid(q, fields = fields, create=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_paket():
    grid = SQLFORM.grid(db.m_paket, create=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_satuan_menu():
    grid = SQLFORM.grid(db.m_satuan_menu, create=True, csv=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def master_satuan_supplier():
    grid = SQLFORM.grid(db.m_satuan_supplier, create=True, csv=False)
    return dict(grid = grid)

def test():
    x= db(db.m_satuan_menu).select().as_list()
    return dict(id=10, nama='halo', tabel = x)