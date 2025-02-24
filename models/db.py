# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import os
import re

REQUIRED_WEB2PY_VERSION = "3.0.10"

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

web2py_version_string = request.global_settings.web2py_version.split("-")[0]
web2py_version = list(map(int, web2py_version_string.split(".")[:3]))
if web2py_version < list(map(int, REQUIRED_WEB2PY_VERSION.split(".")[:3])):
    raise HTTP(500, f"Requires web2py version {REQUIRED_WEB2PY_VERSION} or newer, not {web2py_version_string}")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True) #AppConfig(reload=True)

if "GAE_APPLICATION" not in os.environ:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get("db.uri"),
             pool_size=configuration.get("db.pool_size"),
             #migrate_enabled=configuration.get("db.migrate"),
             #lazy_tables=True,
             check_reserved=["all"])
else:
    # ---------------------------------------------------------------------
    # connect to Google Firestore
    # ---------------------------------------------------------------------
    db = DAL("firestore")
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be "controller/function.extension"
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get("app.production"):
    response.generic_patterns.append("*")
else:
    response.generic_patterns.append("*")

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = "bootstrap4_inline"
response.form_label_separator = ""

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = "concat,minify,inline"
# response.optimize_js = "concat,minify,inline"

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = "0.0.0"

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get("host.names"))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields["auth_user"] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = "logging" if request.is_local else configuration.get("smtp.server")
mail.settings.sender = configuration.get("smtp.sender")
mail.settings.login = configuration.get("smtp.login")
mail.settings.tls = configuration.get("smtp.tls") or False
mail.settings.ssl = configuration.get("smtp.ssl") or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.long_expiration = 3600*24*30 # one month
auth.settings.remember_me_form = False
# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get("app.author")
response.meta.description = configuration.get("app.description")
response.meta.keywords = configuration.get("app.keywords")
response.meta.generator = configuration.get("app.generator")
response.show_toolbar = configuration.get("app.toolbar")

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get("google.analytics_id")

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get("scheduler.enabled"):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get("scheduler.heartbeat"))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table("mytable", Field("myfield", "string"))
#
# Fields can be "string","text","password","integer","double","boolean"
#       "date","time","datetime","blob","upload", "reference TABLENAME"
# There is an implicit "id integer autoincrement" field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield="value")
# >>> rows = db(db.mytable.myfield == "value").select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

jenis_kelamin = ['Laki-laki', 'Perempuan']

db.define_table('m_propinsi',
    Field('propinsi', 'string'),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_kabupaten_kota',
    Field('id_propinsi', reference = IS_IN_DB(db, db.m_propinsi.id,'%(propinsi)s' )),
    Field('kabupaten_kota', 'string'),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_kecamatan',
    Field('id_kabupaten_kota', reference = IS_IN_DB(db, db.m_kabupaten_kota.id,'%(kabupaten_kota)s' )),
    Field('kecamatan', 'string'),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_kelurahan_desa',
    Field('id_kecamatan', reference = IS_IN_DB(db, db.m_kecamatan.id,'%(kecamatan)s' )),
    Field('kelurahan_desa', 'string'),
    #Field('kode_pos', 'integer'),
    Field('deleted', 'boolean', default=False)
    )
db.define_table('m_kodepos',
    Field('id_kelurahan_desa', reference = IS_IN_DB(db, db.m_kelurahan_desa.id,'%(kelurahan_desa)s' )),
    Field('id_kecamatan', reference = IS_IN_DB(db, db.m_kecamatan.id,'%(kecamatan)s' )),
    Field('id_kabupaten_kota', reference = IS_IN_DB(db, db.m_kabupaten_kota.id,'%(kabupaten_kota)s' )),
    Field('id_propinsi', reference = IS_IN_DB(db, db.m_propinsi.id,'%(propinsi)s' )),
    Field('kode_pos', 'string'),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_paket', 
    Field('id_vendor', 'integer'),
    Field('nama_paket', 'string'),
    Field('pagu_harga', 'integer'),
    Field('kalori', 'float'),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

#tentang struktur sekolak - disdik. include kepsek dan admin disdik
db.define_table('m_sekolah',
    Field('nama_sekolah', 'string'),
    Field('alamat', 'string'),
    Field('id_kelurahan_desa', 'reference m_kelurahan_desa', requires=IS_IN_DB(db, db.m_kelurahan_desa.id, '%(kelurahan_desa)s'), default=None),
    Field('id_kode_pos', 'reference m_kodepos', requires=IS_IN_DB(db, db.m_kodepos.id, '%(kode_pos)s'), default=None),
    # Field('id_kecamatan', 'reference m_kecamatan', requires=IS_IN_DB(db, 'm_kecamatan.id', '%(kecamatan)s')),
    # Field('id_kabupaten_kota', 'reference m_kabupaten_kota', requires=IS_IN_DB(db, 'm_kabupaten_kota.id', '%(kabupaten_kota)s')),
    # Field('id_propinsi', 'reference m_propinsi', requires=IS_IN_DB(db, 'm_propinsi.id', '%(propinsi)s')),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )

db.define_table('m_disdik',
    Field('nama_disdik', 'string'),
    Field('alamat', 'string'),
    Field('id_kelurahan_desa', 'reference m_kelurahan_desa', requires=IS_IN_DB(db, db.m_kelurahan_desa.id, '%(kelurahan_desa)s'), default=None),
    Field('id_kode_pos', 'reference m_kodepos', requires=IS_IN_DB(db, db.m_kodepos.id, '%(kode_pos)s'), default=None),
    # Field('id_kecamatan', 'reference m_kecamatan', requires=IS_IN_DB(db, 'm_kecamatan.id', '%(kecamatan)s')),
    # Field('id_kabupaten_kota', 'reference m_kabupaten_kota', requires=IS_IN_DB(db, 'm_kabupaten_kota.id', '%(kabupaten_kota)s')),
    # Field('id_propinsi', 'reference m_propinsi', requires=IS_IN_DB(db, 'm_propinsi.id', '%(propinsi)s')),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )

db.define_table('map_disdik_sekolah',
    Field('id_sekolah', reference = IS_IN_DB(db, db.m_sekolah.id,'%(nama_sekolah)s' )),
    Field('id_disdik', reference = IS_IN_DB(db, db.m_disdik.id, '%(nama_disdik)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    )

db.define_table('map_sekolah_kepala',
    Field('id_sekolah', reference = IS_IN_DB(db, db.m_sekolah.id,'%(nama_sekolah)s' )),
    Field('id_kepala_sekolah', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    )

db.define_table('map_admin_disdik',
    Field('id_disdik', reference = IS_IN_DB(db, db.m_disdik.id,'%(nama_disdik)s' )),
    Field('id_admin', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    )

db.define_table('m_supplier',
    Field('nama_supplier', 'string'),
    Field('alamat', 'string'),
    Field('id_kelurahan_desa', 'reference m_kelurahan_desa', requires=IS_IN_DB(db, db.m_kelurahan_desa.id, '%(kelurahan_desa)s'), default=None),
    Field('id_kode_pos', 'reference m_kodepos', requires=IS_IN_DB(db, db.m_kodepos.id, '%(kode_pos)s'), default=None),
    # Field('id_kecamatan', 'reference m_kecamatan', requires=IS_IN_DB(db, 'm_kecamatan.id', '%(kecamatan)s')),
    # Field('id_kabupaten_kota', 'reference m_kabupaten_kota', requires=IS_IN_DB(db, 'm_kabupaten_kota.id', '%(kabupaten_kota)s')),
    # Field('id_propinsi', 'reference m_propinsi', requires=IS_IN_DB(db, 'm_propinsi.id', '%(propinsi)s')),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False),
    )

db.define_table('map_supplier_user',
    Field('id_supplier', reference = IS_IN_DB(db, db.m_supplier.id,'%(nama_supplier)s' )),
    Field('id_user', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )

db.define_table('m_vendor',
    Field('nama_vendor', 'string'),
    Field('alamat', 'string'),
    Field('id_kelurahan_desa', 'reference m_kelurahan_desa', requires=IS_IN_DB(db, db.m_kelurahan_desa.id, '%(kelurahan_desa)s'), default=None),
    Field('id_kode_pos', 'reference m_kodepos', requires=IS_IN_DB(db, db.m_kodepos.id, '%(kode_pos)s'), default=None),
    # Field('id_kecamatan', 'reference m_kecamatan', requires=IS_IN_DB(db, 'm_kecamatan.id', '%(kecamatan)s')),
    # Field('id_kabupaten_kota', 'reference m_kabupaten_kota', requires=IS_IN_DB(db, 'm_kabupaten_kota.id', '%(kabupaten_kota)s')),
    # Field('id_propinsi', 'reference m_propinsi', requires=IS_IN_DB(db, 'm_propinsi.id', '%(propinsi)s')),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('map_vendor_user',
    Field('id_vendor', reference = IS_IN_DB(db, db.m_vendor.id,'%(nama_vendor)s' )),
    Field('id_user', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('map_vendor_sekolah',
    Field('id_vendor', reference = IS_IN_DB(db, db.m_vendor.id,'%(nama_vendor)s' )),
    Field('id_sekolah', reference = IS_IN_DB(db, db.m_sekolah.id,'%(nama_sekolah)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_satuan_menu',
    Field('nama_satuan', 'string'),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('m_satuan_supplier',
    Field('nama_satuan', 'string'),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )


# db.define_table('t_translate_satuan',
#     Field('id_supplier', reference = IS_IN_DB(db, db.m_supplier.id)),
#     Field('id_satuan_menu', reference = IS_IN_DB(db, db.m_satuan_menu.id)),
#     Field('id_satuan_supplier', reference = IS_IN_DB(db, db.m_satuan_supplier.id)),
#     )

db.define_table('t_siswa',
    Field('id_sekolah', reference = IS_IN_DB(db, db.m_sekolah.id,'%(nama_sekolah)s' )),
    Field('nama', 'string'),
    Field('tempat_lahir', 'string'),
    Field('tanggal_lahir','date'),
    Field('jenis_kelamin', requires=IS_IN_SET(jenis_kelamin, zero=None), default = jenis_kelamin[0]),
    #Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )

db.define_table('t_periksa_siswa',
    Field('id_siswa', reference = IS_IN_DB(db, db.t_siswa.id,'%(nama)s' )),
    Field('tinggi_badan', 'float'),
    Field('berat_badan', 'float'),
    Field('tanggal_pengukuran', 'date'),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)    
    )

db.define_table('t_harga_supplier',
    Field('id_supplier', reference = IS_IN_DB(db, db.m_supplier.id, '%(nama_supplier)s' )),
    Field('nama_item', 'string'),
    Field('volume', 'integer'),
    Field('harga', 'integer'),
    Field('id_satuan_supplier', reference = IS_IN_DB(db, db.m_satuan_supplier.id, '%(nama_satuan)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('t_pembelian_bahan',
    Field('id_supplier', reference = IS_IN_DB(db, db.m_supplier.id,'%(nama_supplier)s' )),
    Field('id_vendor', reference = IS_IN_DB(db, db.map_vendor_user.id,'%(id_vendor)s' )),
    Field('nama_vendor', reference = IS_IN_DB(db, db.m_vendor.id,'%(nama_vendor)s' )),
    Field('nama_item', 'string'),
    Field('volume', 'integer'),
    Field('harga', 'integer', reference = IS_IN_DB(db, db.t_harga_supplier.id,'%(harga)s' )),
    Field('id_satuan_supplier', reference = IS_IN_DB(db, db.m_satuan_supplier.id,'%(nama_satuan)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('sudah_diterima', 'boolean', default=False),
    Field('deleted', 'boolean', default=False)
)

# db.define_table('t_paket_menu',
#     Field('id_paket', reference = IS_IN_DB(db, db.m_paket.id,'%(nama_sekolah)s' )),
#     Field('menu', 'string'),
#     Field('id_m_satuan_menu', reference = IS_IN_DB(db, db.m_satuan_menu.id,'%(nama_satuan)s' )),
#     Field('id_supplier', reference = IS_IN_DB(db, db.m_supplier.id,'%(nama_supplier)s' )),
#     )


db.define_table('t_pengajuan_paket',
    Field('id_paket', reference = IS_IN_DB(db, db.m_paket.id,'%(nama_paket)s' )),
    Field('jumlah', 'integer'),
    Field('approve', 'boolean', default=False),
    Field('id_pengaju', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('id_approver', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp_setuju', 'datetime', default=None),
    Field('id_vendor', reference = IS_IN_DB(db, db.m_vendor.id,'%(nama_vendor)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('t_pemberian_paket',
    Field('id_paket', reference = IS_IN_DB(db, db.m_paket.id,'%(nama_paket)s' )),
    Field('jumlah', 'integer'),
    Field('id_tujuan', reference = IS_IN_DB(db, db.m_sekolah.id,'%(nama_sekolah)s' )),
    Field('id_user', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('tanggal_pengiriman', 'date', requires = IS_NOT_EMPTY(error_message='Tanggal harus diisi!')),
    Field('id_vendor', reference = IS_IN_DB(db, db.m_vendor.id,'%(nama_vendor)s' )),
    Field('tanggal_pengiriman_dari_vendor', 'date'),
    Field('jumlah_dari_vendor', 'integer'),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('t_tanda_terima_paket',
    Field('id_t_pemberian_paket', reference = IS_IN_DB(db, db.t_pemberian_paket.id,'%(jumlah)s' )),
    Field('jumlah', 'integer', label='Jumlah Diterima'),
    Field('tanggal_terima', 'string'),
    Field('id_user', reference = IS_IN_DB(db, db.auth_user.id,'%(first_name)s' )),
    Field('time_stamp', 'datetime', default = request.now),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('t_belanja_vendor_item',
    Field('id_t_pengajuan_paket'),
    Field('id_t_harga_supplier'),
    Field('deleted', 'boolean', default=False)
    )

db.define_table('t_laporan_masyarakat',
    Field('uraian', 'text'),
    Field('time_stamp', 'datetime', default = request.now),
    )

# def get_alamat_by_kode_pos(kodepos):
#     ret ={}
#     alam=db((db.m_propinsi.id==db.m_kabupaten_kota.id_propinsi) & 
#         (db.m_kabupaten_kota.id==db.m_kecamatan.id_kabupaten_kota)&
#         (db.m_kecamatan.id==db.m_kelurahan_desa.id_kecamatan)&
#         (db.m_kelurahan_desa.kodepos==kodepos)).select().as_list()
#     if len(alam) == 1:
#         ret=alam[0]

#     return ret

def get_alamat_by_kode_pos_id(id_kodepos):
    ret ={}
    alam=db((db.m_kodepos.id==id_kodepos)&
        (db.m_kelurahan_desa.id == db.m_kodepos.id_kelurahan_desa)&
        (db.m_kecamatan.id == db.m_kodepos.id_kecamatan)&
        (db.m_kabupaten_kota.id == db.m_kodepos.id_kabupaten_kota)&
        (db.m_propinsi.id == db.m_kodepos.id_propinsi)
        ).select().as_list()
    if len(alam) == 1:
        ret=alam[0]

    return ret


def cors_origin():
    origin = request.env.http_origin
    headers = {}
    headers['Access-Control-Allow-Origin'] = origin
    headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST, HEAD, PUT'
    headers['Access-Control-Allow-Headers'] = 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization,Accept'
    headers['Access-Control-Allow-Credentials'] = 'true';
    response.headers.update(headers)

    if request.env.request_method == 'OPTIONS':
        headers['Content-Type'] = None
        raise HTTP(200, '', **headers)


def cors_allow(action):

    def f(*args, **kwargs):
        cors_origin()
        return action(*args, **kwargs)

    f.__doc__ = action.__doc__
    f.__name__ = action.__name__
    f.__dict__.update(action.__dict__)

    return f
