
@auth.requires_membership('kepala_sekolah')
def tanda_terima_paket():
    import json as json
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    # response.headers['Access-Control-Max-Age'] = '3600'

    sekolahan_saya = db((db.map_sekolah_kepala.id_kepala_sekolah==auth.user.id) &
        (db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id)).select().as_list()
    paket_saya=[]
    nama_sekolah=""
    if len(sekolahan_saya)==1:
        id_sekolahan_saya=sekolahan_saya[0]['m_sekolah']['id']
        nama_sekolah=sekolahan_saya[0]['m_sekolah']['nama_sekolah']
        paket_saya = db(
            (db.t_pemberian_paket.id_paket == db.m_paket.id) &
            (db.t_pemberian_paket.id_tujuan == id_sekolahan_saya) &
            (db.t_pemberian_paket.tanggal_pengiriman_dari_vendor != None) &
            (db.t_pemberian_paket.deleted == False)
            ).select().as_list()
    form = SQLFORM.factory(
        Field('js', 'string')
        )
    if form.process(dbio=False).accepted:
        vv = json.loads(request.vars.js)
        for i in vv:
            db.t_tanda_terima_paket.insert(id_t_pemberian_paket = i['id'], jumlah = i['jumlah'], 
                tanggal_terima = i['tanggal_terima'], id_user= auth.user.id)
    elif form.errors:
        response.flash = 'Ada kesalahan pengisian form'
    else:
        response.flash= "Silahkan isi"
    return dict(form = form, paket_saya = paket_saya, nama_sekolah=nama_sekolah)

@auth.requires_membership('kepala_sekolah')
def tanda_terima_paket_apps():
    sekolahan_saya = db((db.map_sekolah_kepala.id_kepala_sekolah==auth.user.id) &
        (db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id)).select().as_list()
    paket_saya=[]
    nama_sekolah=""
    if len(sekolahan_saya)==1:
        id_sekolahan_saya=sekolahan_saya[0]['m_sekolah']['id']
        nama_sekolah=sekolahan_saya[0]['m_sekolah']['nama_sekolah']
        paket_saya = db((db.t_pemberian_paket.id_paket == db.m_paket.id) &
            (db.t_pemberian_paket.id_tujuan == id_sekolahan_saya) &
            (db.t_pemberian_paket.deleted == False)).select(
            db.t_pemberian_paket.id,
            db.t_pemberian_paket.jumlah,
            db.m_paket.id,
            db.m_paket.nama_paket,
            ).as_list()
    return dict(paket_saya = paket_saya, nama_sekolah=nama_sekolah)

@auth.requires_membership('kepala_sekolah')
def tanda_terima_paket_terima_apps():
    vv = json.loads(request.vars.js)
    for i in vv:
        db.t_tanda_terima_paket.insert(id_t_pemberian_paket = i['id'], jumlah = i['jumlah'], 
            tanggal_terima = i['tanggal_terima'], id_user= auth.user.id)
    return dict(res='ok')

@auth.requires_membership('kepala_sekolah')
def tanda_terima():
    import json as json
    sekolahan_saya = db((db.map_sekolah_kepala.id_kepala_sekolah==auth.user.id) &
        (db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id)).select().as_list()
    paket_saya=[]
    nama_sekolah=""
    if len(sekolahan_saya)==1:
        id_sekolahan_saya=sekolahan_saya[0]['m_sekolah']['id']
        nama_sekolah=sekolahan_saya[0]['m_sekolah']['nama_sekolah']
        paket_saya = db((db.t_pemberian_paket.id_paket == db.m_paket.id) &
            (db.t_pemberian_paket.id_tujuan == id_sekolahan_saya) &
            (db.t_pemberian_paket.deleted == False)).select().as_list()
    form = SQLFORM.factory(
        Field('js', 'string')
        )
    if form.process(dbio=False).accepted:
        vv = json.loads(request.vars.js)
        for i in vv:
            db.t_tanda_terima_paket.insert(id_t_pemberian_paket = i['id'], jumlah = i['jumlah'], 
                tanggal_terima = i['tanggal_terima'], id_user= auth.user.id)
    elif form.errors:
        response.flash = 'Ada kesalahan pengisian form'
    else:
        response.flash= "Silahkan isi"
    return response.json(dict(form = form, paket_saya = paket_saya, nama_sekolah=nama_sekolah))


@auth.requires_membership('kepala_sekolah')
def status_siswa():
    sekolahan_saya = db((db.map_sekolah_kepala.id_kepala_sekolah == auth.user.id)&(db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id)).select().as_list()
    grid=None
    if len(sekolahan_saya)==1:
        #siswa_saya=db(db.t_siswa.id_sekolah==sekolahan_saya['m_sekolah']['id']).select(orderby=db.t_siswa.nama).as_list()
        db.t_siswa.id.readable=False
        db.t_siswa.id.writable=False
        links = [
            dict(header='Detail',body=lambda row: A("Lihat pemeriksaan", _href = URL('sekolah', 'siswa_periksa', vars=dict(id=row.id) ) ))
            ]
        fields=(db.t_siswa.id, db.t_siswa.nama, db.t_siswa.jenis_kelamin)

        headers={'t_siswa.nama':'Nama Siswa', 't_siswa.jenis_kelamin':'Jenis Kelamin'}

        grid = SQLFORM.grid((db.t_siswa.id_sekolah==sekolahan_saya[0]['m_sekolah']['id']),
            links=links,
            fields=fields,
            headers=headers,
            searchable=True, editable=False, deletable=False, csv=False, details=False)
    return dict(grid=grid)

@auth.requires_membership('kepala_sekolah')
def siswa_periksa():
    import json as json
    #from datetime import datetime
    data = db(db.t_periksa_siswa.id_siswa==request.vars.id).select().as_list()
    data_js=[]
    for d in data:
        data_js.append(dict(tinggi_badan=d['tinggi_badan'], berat_badan=d['berat_badan'], tanggal_pengukuran=d['tanggal_pengukuran'].strftime('%d-%m-%Y')))
    info_siswa = db(db.t_siswa.id==request.vars.id).select().as_list()
    return dict(data=data, info_siswa = info_siswa, data_js=XML(json.dumps(data_js)))

@auth.requires_membership('kepala_sekolah')
def pengajuan_paket_makan():
    #mencari disdik dimana kepsek bertugas
    id_disdik = db((db.map_disdik_sekolah.id_sekolah == db.m_sekolah.id)&(db.map_disdik_sekolah.id_disdik == db.m_disdik.id) &
        (db.map_admin_disdik.id_disdik == db.m_disdik.id)&(db.map_admin_disdik.id_admin == db.auth_user.id) &
        (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id)&(db.map_sekolah_kepala.id_kepala_sekolah == auth.user.id)
        ).select().as_list()

    form = SQLFORM.factory(
        Field('paket_makan', 'integer', requires = IS_IN_DB(db, db.m_paket.id, '%(nama_paket)s')),
        Field('jumlah_paket', 'integer'),
        )

    if form.process(dbio=False).accepted:
        item = {}
        item['id_paket'] = request.vars.paket_makan
        item['id_pengaju'] = auth.user.id
        item['jumlah'] = request.vars.jumlah_paket
        item['id_approver'] = id_disdik[0]['auth_user']['id']
        db.t_pengajuan_paket.insert(**item)
    elif form.errors:
        response.flash = 'Ada kesalahan pengisian form'
    else:
        response.flash= "Silahkan isi"

    return dict(form = form)

@auth.requires_membership('super_admin')
def map_sekolah_disdik():
    form = SQLFORM.factory(
        Field ('nama_sekolah', 'integer', requires = IS_IN_DB(db, db.m_sekolah.id, '%(nama_sekolah)s')),
        Field ('nama_disdik', 'integer', requires = IS_IN_DB(db, db.m_disdik.id, '%(nama_disdik)s')),
        )
    if form.process(dbio=False).accepted:
        item = {}
        item['id_sekolah'] = request.vars.nama_sekolah
        item['id_disdik'] = request.vars.nama_disdik
        db.map_disdik_sekolah.insert(**item)
    return dict(form = form)

@auth.requires_membership('super_admin')
def list_map_sekolah_disdik():
    fields = (db.m_sekolah.nama_sekolah, db.m_sekolah.alamat, db.m_disdik.nama_disdik,db.m_disdik.alamat)
    grid = SQLFORM.grid((db.map_disdik_sekolah.id_sekolah==db.m_sekolah.id) & (db.map_disdik_sekolah.id_disdik==db.m_disdik.id),
        fields = fields,
        create=False, deletable=False, csv=False, editable=False, details=False)
    return dict(grid = grid)

@auth.requires_membership('super_admin')
def map_sekolah_kepala():
    group = db(db.auth_group.role=='kepala_sekolah').select().as_list()
    daftar_total = db((db.auth_user.id == db.auth_membership.user_id) & (db.auth_membership.group_id==group[0]['id'])).select().as_list()
    daftar_kepsek = []
    for dt in daftar_total:
        daftar_kepsek.append( (dt['auth_user']['id'] , dt['auth_user']['first_name']+" "+ dt['auth_user']['last_name']) )

    form = SQLFORM.factory(
        Field ('nama_kepala_sekolah', 'integer', requires = IS_IN_SET(daftar_kepsek)),
        Field ('nama_sekolah', 'integer', requires = IS_IN_DB(db, db.m_sekolah.id, '%(nama_sekolah)s')),
        )

    if form.process(dbio=False).accepted:
        item = {}
        item['id_kepala_sekolah'] = request.vars.nama_kepala_sekolah
        item['id_sekolah'] = request.vars.nama_sekolah
        db.map_sekolah_kepala.insert(**item)
    return dict(form = form)

@auth.requires_membership('super_admin')
def list_map_sekolah_kepala():
    fields = (db.m_sekolah.nama_sekolah, db.m_sekolah.alamat, db.auth_user.first_name, db.auth_user.last_name)
    grid = SQLFORM.grid((db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id) & (db.map_sekolah_kepala.id_kepala_sekolah==db.auth_user.id),
        fields = fields,
        create=False, deletable=False, csv=False, editable=False, details=False)
    return dict(grid = grid)
