# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    if auth.user is not None:
        redirect(URL('index2'))
    else:
        response.flash = T("Selamat datang")
    return dict(message=T('Welcome to Mambo!'), status='front_page')


def index2():
    if auth.user == None:
        redirect(URL('index'))
    return dict(a='Selamat beraktivitas')

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

def auto_region_web():
    import json as json
    ret = db( (db.m_kelurahan_desa.kelurahan_desa.like('%'+request.vars.term.upper()+'%')) &
        (db.m_kelurahan_desa.id_kecamatan==db.m_kecamatan.id)&
        (db.m_kecamatan.id_kabupaten_kota==db.m_kabupaten_kota.id)&
        (db.m_kabupaten_kota.id_propinsi==db.m_propinsi.id)&
        (db.m_kodepos.id_kelurahan_desa==db.m_kelurahan_desa.id)
        ).select(limitby=(0,9)).as_list()
    return XML(json.dumps(ret))

# def auto_propinsi_web():
#     import json as json
#     ret = db((db.m_propinsi.propinsi.like('%'+request.vars.term.upper()+'%'))).select(limitby=(0,9)).as_list()    
#     return XML(json.dumps(ret))


# def auto_kabupaten_kota_web():
#     import json as json
#     ret = db( (db.m_kabupaten_kota.kabupaten_kota.like('%'+request.vars.term.upper()+'%')) &
#             (db.m_kabupaten_kota.id_propinsi==request.vars.id_propinsi)
#         ).select(limitby=(0,9)).as_list()
#     return XML(json.dumps(ret))

# def auto_kecamatan_web():
#     import json as json
#     ret = db( (db.m_kecamatan.kecamatan.like('%'+request.vars.term.upper()+'%')) &
#         (db.m_kecamatan.id_kabupaten_kota==request.vars.id_kabupaten_kota)
#         ).select(limitby=(0,9)).as_list()
#     return XML(json.dumps(ret))

# def auto_kelurahan_desa_web():
#     import json as json
#     ret = db( (db.m_kelurahan_desa.kelurahan_desa.like('%'+request.vars.term.upper()+'%')) &
#         (db.m_kelurahan_desa.id_propinsi==request.vars.id_propinsi)
#         ).select(limitby=(0,9)).as_list()
#     return XML(json.dumps(ret))

# def auto_kodepos():
#     import json as json
#     ret = db( (db.m_kodepos.kode_pos.like('%'+request.vars.term.upper()+'%')) &
#         (db.m_kabupaten_kota.id_propinsi==request.vars.id_propinsi)
#         ).select(limitby=(0,9)).as_list()
#     return XML(json.dumps(ret))

def test_autocomplete():

    return dict(a='a')
# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# def test_koneksi():
#     links = [
#         dict(header='Detail',body=lambda row: A("Lihat pemeriksaan", _href = URL('default', 'test_periksa', vars=dict(id=row.id) ) ))
#         ]

#     grid = SQLFORM.grid((db.t_siswa.id_sekolah),
#         links=links,
#         searchable=True, editable=False, deletable=False, csv=False, details=False)
#     return dict(grid=grid)

# def test_periksa():
#     data = db(db.t_periksa_siswa.id_siswa==request.vars.id).select().as_list()
#     return dict(data=data)
    
def debug_t():
    a = dict(aa='cc')
    return dict(res='ok')
    
def download():
    return response.download(request, db)
