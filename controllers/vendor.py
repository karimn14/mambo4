@auth.requires_membership('super_admin')
def map_vendor_user_id():
    group = db(db.auth_group.role=='vendor').select().as_list()
    daftar_total = db((db.auth_user.id == db.auth_membership.user_id) & (db.auth_membership.group_id==group[0]['id'])).select().as_list()
    daftar_vendor = []
    for dt in daftar_total:
        daftar_vendor.append( (dt['auth_user']['id'] , dt['auth_user']['first_name']+" "+ dt['auth_user']['last_name']) )

    form = SQLFORM.factory(
        Field ('nama_user', 'integer', requires = IS_IN_SET(daftar_vendor)),
        Field ('nama_vendor', 'integer', requires = IS_IN_DB(db, db.m_vendor.id, '%(nama_vendor)s')),
        )

    if form.process(dbio=False).accepted:
        item = {}
        item['id_user'] = request.vars.nama_user
        item['id_vendor'] = request.vars.nama_vendor
        db.map_vendor_user.insert(**item)
    return dict(form = form)

@auth.requires_membership('super_admin')
def list_map_vendor_user_id():
    fields = (db.m_vendor.nama_vendor, db.m_vendor.alamat, db.auth_user.first_name, db.auth_user.last_name)
    q = ((db.m_vendor.id==db.map_vendor_user.id_vendor) & (db.map_vendor_user.id_user==db.auth_user.id))
    grid = SQLFORM.grid(q,
        fields = fields,
        create=False, deletable=False, csv=False, editable=False, details=False)

    #grid = SQLFORM.smartgrid(db.map_vendor_user, linked_tables=['m_vendor','auth_user'])
    return dict(grid = grid)

def list_map_vendor_sekolah():
    fields = (db.m_vendor.nama_vendor, db.m_vendor.alamat, db.m_sekolah.nama_sekolah, db.m_sekolah.alamat)
    grid = SQLFORM.grid((db.map_vendor_sekolah.id_vendor==db.m_vendor.id) & (db.map_vendor_sekolah.id_sekolah==db.m_sekolah.id),
        fields = fields,
        create=False, deletable=False, csv=False, editable=False, details=False)
    return dict(grid = grid)

@auth.requires_membership('vendor')
def item_supplier():
    form = SQLFORM.factory(
        Field('nama_barang', 'string', requires = IS_NOT_EMPTY('Harus diisi')),
        Field('harga', 'integer', requires = IS_NOT_EMPTY('Harus diisi')),
        Field('volume', 'integer', requires = IS_NOT_EMPTY('Harus diisi')),
        Field('satuan', 'integer', requires = IS_IN_DB(db, db.m_satuan_supplier.id, '%(nama_satuan)s')),
        )

    if form.process(dbio=False).accepted:
        item = {}
        item['nama_item'] = request.vars.nama_barang
        item['id_supplier'] = auth.user.id
        item['volume'] = request.vars.volume
        item['harga'] = request.vars.harga
        item['id_satuan_supplier'] = request.vars.satuan
        db.t_harga_supplier.insert(**item)
    else:
        response.flash= "Ada kesalahan dalam mengisi form"

    return dict(form = form)


@auth.requires_membership('vendor')
def pesanan():
    vendor_saya1 = db((db.map_vendor_user.id_vendor == db.m_vendor.id ) & (db.map_vendor_user.id_user == auth.user.id)).select().as_list()
    id_vendor=None

    if len(vendor_saya1)==1:
        id_vendor = vendor_saya1[0]['m_vendor']['id']
        print (id_vendor)

    q = ((db.t_pemberian_paket.id_vendor == id_vendor) &
        (db.t_pemberian_paket.tanggal_pengiriman_dari_vendor == None) &
        #(db.m_vendor.id == db.map_vendor_user.id_vendor) &
        #(db.map_vendor_user.id_user == auth.user.id) &
        (db.t_pemberian_paket.id_tujuan == db.m_sekolah.id) &
        (db.t_pemberian_paket.id_paket == db.m_paket.id))
    fields = (db.t_pemberian_paket.id, db.t_pemberian_paket.tanggal_pengiriman, db.m_sekolah.nama_sekolah, db.m_paket.nama_paket, db.m_paket.pagu_harga, db.t_pemberian_paket.jumlah)
    links = [
        dict(header='Harga Total',body=lambda row: SPAN(row.t_pemberian_paket.jumlah * row.m_paket.pagu_harga) ),
        dict(header='Pengiriman',body=lambda row: A("Kirim pesanan", _href = URL('vendor', 'kirim_pesanan', vars=dict(id=row.t_pemberian_paket.id) ) ))
        ]

    grid = SQLFORM.grid(q, 
        links = links,
        fields = fields,
        create=False, deletable=False, csv=False, editable=False, details=False)
    return dict(grid=grid)

@auth.requires_membership('vendor')
def kirim_pesanan():
    q = ((db.t_pemberian_paket.id == request.vars.id) &
        #(db.m_vendor.id == db.map_vendor_user.id_vendor) &
        #(db.map_vendor_user.id_user == auth.user.id) &
        (db.t_pemberian_paket.id_tujuan == db.m_sekolah.id) &
        (db.t_pemberian_paket.id_paket == db.m_paket.id))
    pesanan = db(q).select().as_list()

    return dict(pesanan = pesanan)

@auth.requires_membership('vendor')
def kirim_sekarang():
    id=request.vars.id
    #print(request.vars)
    db(db.t_pemberian_paket.id==id).update(tanggal_pengiriman_dari_vendor=request.now, jumlah_dari_vendor=request.vars.jumlah)
    
    return dict(a='a')

# def pesanan():
#     #id_vendor = db(db.map_vendor_user.id_user==auth.user.id)
#     query = ((db.t_pengajuan_paket.id_paket == db.m_paket.id)
#         & (db.t_pengajuan_paket.approve == True)
#         & (db.map_sekolah_kepala.id_kepala_sekolah == db.t_pengajuan_paket.id_pengaju)
#         & (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id)
#         & (db.t_pengajuan_paket.id_vendor == db.m_vendor.id)
#         & (db.map_vendor_user.id_vendor == db.m_vendor.id)
#         & (db.map_vendor_user.id_user == auth.user.id)
#         )
#     fields = (db.t_pengajuan_paket.id, db.t_pengajuan_paket.time_stamp, db.m_sekolah.nama_sekolah, db.m_paket.nama_paket, db.m_paket.pagu_harga, db.t_pengajuan_paket.jumlah)
#     links = [
#         dict(header='Harga',body=lambda row: SPAN(row.t_pengajuan_paket.jumlah * row.m_paket.pagu_harga) ),
#         dict(header='Proses',body=lambda row: A("Proses pesanan", _href = URL('vendor', 'proses_pesanan', vars=dict(id=row.t_pengajuan_paket.id) ) ))
#         ]

#     grid = SQLFORM.grid(query, links = links,
#         fields = fields,
#         create=False, deletable=False, csv=False, editable=False, details=False)
#     return dict(grid=grid)


# def proses_pesanan():
#     id = request.vars.id
#     query = ((db.t_pengajuan_paket.id_paket == db.m_paket.id)
#         & (db.t_pengajuan_paket.approve == True)
#         & (db.map_sekolah_kepala.id_kepala_sekolah == db.t_pengajuan_paket.id_pengaju)
#         & (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id)
#         & (db.t_pengajuan_paket.id_vendor == db.m_vendor.id)
#         & (db.map_vendor_user.id_vendor == db.m_vendor.id)
#         & (db.map_vendor_user.id_user == db.auth_user.id)
#         & (db.t_pengajuan_paket.id == id)
#         )
#     pesanan = db(query).select().as_list()[0]

#     q=((db.t_harga_supplier.id_supplier == db.m_supplier.id)
#         )

#     suppliers=db(q).select().as_list()
#     for s in suppliers:
#         s['t_harga_supplier'].pop("time_stamp")
#     supplier_list =  db(db.m_supplier).select().as_list()

#     return dict(list = suppliers, pesanan = pesanan, supplier_list=supplier_list )

