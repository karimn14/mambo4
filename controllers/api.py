import sys
sys.path.append(r"C:\Users\Windows 10\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages")

# import jwt
# from datetime import datetime, timedelta, timezone
# from passlib.context import CryptContext
# from pydantic import BaseModel

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     hashed_password: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def authenticate_user(email: str, password: str):
#     user = db(db.auth_user.email == email).select().first()
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return dict(res="Incorrect Password")
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

@request.restful()
@cors_allow
def login():
    response.view = 'generic.json'
    def POST(*args, **vars):
        email = request.vars.email
        password = request.vars.password
        user = authenticate_user(email, password)
        if not user:
            return dict(error="Incorrect email or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return dict(access_token=access_token, token_type="bearer")
    return locals()

#------------------------------------------------------------------------------------
## barre login
@request.restful()
@cors_allow
def api_login():
    response.view = 'generic.json'
    def GET(*args, **vars):        
        u_name = request.vars.u
        pw = request.vars.pw
        test = auth.login_bare(u_name,pw)
        if test!=False:
            #sanitize data
            role = db((db.auth_membership.user_id==test['id'])&(db.auth_membership.group_id==db.auth_group.id)).select().as_list()
            test.pop('password')
            test.pop('reset_password_key')
            test.pop('registration_key')
            test.pop('registration_id')
            test['role']=role[0]['auth_group']['role']
        return dict(status=test)        
    return locals()

#------------------------------------------------------------------------------------
## untuk disdik
#------------------------------------------------------------------------------------
#Added: Arga 15-02-2025
def f_cek_id_disdik(t_id):
    disdik_saya = []
    id_disdik=None
    nama_disdik = 'Disdik Debug'

    if t_id!=None:
        disdik_saya = db((db.map_admin_disdik.id_admin == db.auth_user.id) & 
            (db.map_admin_disdik.id_disdik==db.m_disdik.id)& 
            (db.auth_user.id == t_id)).select().as_list()
    else:
       id_user=dict(id=3, first_name='Disdik', last_name='Regional') 


    if len(disdik_saya)==1:
        id_disdik = disdik_saya[0]['m_disdik']['id']
        nama_disdik = disdik_saya[0]['m_disdik']['nama_disdik']
        id_kelurahan_desa=disdik_saya[0]['m_disdik']['id_kelurahan_desa']
        id_kode_pos=disdik_saya[0]['m_disdik']['id_kode_pos']
        id_user=dict(id=disdik_saya[0]['auth_user']['id'], first_name=disdik_saya[0]['auth_user']['first_name'], 
            last_name=disdik_saya[0]['auth_user']['last_name'])        
    else:
        id_disdik=1
        nama_disdik = 'Disdik Debug'
        id_kelurahan_desa=0
        id_kode_pos=0
        id_user=dict(id=3, first_name='Disdik', last_name='Regional') 
    return dict(id_disdik=id_disdik, nama_disdik=nama_disdik, id_kelurahan_desa =id_kelurahan_desa, 
        id_kode_pos=id_kode_pos, user=id_user)

##### Untuk ke web:
#Added: Arga 15-02-2025
@request.restful()
@cors_allow
def data_penerimaan_paket_dari_kepsek():

    response.view = 'generic.json'
    def GET(*args, **vars):
        if request.vars.id_user==None:
            raise HTTP(400)
        profil = f_cek_id_disdik(request.vars.id_user)
        #cari sekolahan dibawah disdik saya:
        list_sekolah = db(db.map_disdik_sekolah.id_disdik==profil['id_disdik']).select().as_list()
        
        paket_sekolah_sekolah=[]
        print("-------------------------------------------")
        for l in list_sekolah:
            ps = db(
                (db.t_pemberian_paket.id_paket == db.m_paket.id) &
                (db.t_pemberian_paket.id_tujuan == l['id_sekolah']) &
                (db.t_pemberian_paket.id == db.t_tanda_terima_paket.id_t_pemberian_paket) &
                #(db.t_pemberian_paket.tanggal_pengiriman_dari_vendor != None) &
                (db.t_pemberian_paket.deleted == False)
                ).select().as_list()
            for p in ps:
                #sanitizing response:
                p['t_pemberian_paket'].pop('time_stamp')
                p['t_pemberian_paket'].pop('id_vendor')
                p['t_pemberian_paket'].pop('id_paket')
                p['t_pemberian_paket'].pop('deleted')
                p['t_tanda_terima_paket'].pop('time_stamp')
                p['t_tanda_terima_paket'].pop('deleted')
                p['m_paket'].pop('time_stamp')
                p['m_paket'].pop('deleted')


            sek = db(db.m_sekolah.id==l['id_sekolah']).select().as_list()
            if len(sek)==1:
                kep=dict(first_name=None, last_name=None)
                kepsek = db((db.map_sekolah_kepala.id_sekolah == l['id_sekolah'])&
                    (db.map_sekolah_kepala.id_kepala_sekolah == db.auth_user.id)
                    ).select().as_list()
                if len(kepsek)==1:
                    kep['first_name']=kepsek[0]['auth_user']['first_name']
                    kep['last_name']=kepsek[0]['auth_user']['last_name']
                #sanitizing response:
                sek[0].pop('time_stamp')
                sek[0].pop('deleted')
                rr = dict(sekolah = sek[0], paket=ps, kepala_sekolah = kep)

                paket_sekolah_sekolah.append(rr)
        return dict(test = paket_sekolah_sekolah)
    return locals()    

#disdik auth_user.id_user=3
def get_disdik_id(t_id=None):
    # Fetch disdik data
    disdik_data = db((db.map_disdik_user.id_user == db.auth_user.id) & 
                     (db.map_disdik_user.id_disdik == db.m_disdik.id) & 
                     (db.auth_user.id == t_id)).select().first()
    
    if not disdik_data:
        return dict(error="Disdik not found")

    # Ensure id_disdik is valid
    if not disdik_data.m_disdik.id:
        return dict(error="Invalid Disdik ID")

    id_disdik = disdik_data.m_disdik.id
    return id_disdik

@request.restful()
@cors_allow
def disdik_menu():
    response.view = 'generic.json'
    def GET(*args, **vars):
   
        menus = db(db.m_paket).select().as_list()
        return dict(menus=menus)
    return locals()


@request.restful()
@cors_allow
def disdik_kontrak():

    response.view = 'generic.json'

    def GET(*args, **vars):

        db_now = db.t_kontrak_disdik.select().as_list()
        return dict(kontrak=db_now)

    def POST(*args, **vars):
        required_vars = ['id_user', 'id_vendor', 'nama', 'nip_npwp', 'jabatan', 
                         'alamat', 'instansi', 'jenis_paket', 'jumlah_kalori', 
                         'jumlah_paket_per_hari', 'tanggal_mulai', 'tanggal_selesai', 
                         'total_biaya_kontrak', 'bukti_kontrak']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        id_disdik = get_disdik_id(request.vars.id_user)

        db.t_kontrak_disdik.insert(
            id_disdik= id_disdik,
            id_vendor=request.vars.id_vendor,
            nama=request.vars.nama,
            nip_npwp=request.vars.nip_npwp,
            jabatan=request.vars.jabatan,
            alamat=request.vars.alamat,
            instansi=request.vars.instansi,
            jenis_paket=request.vars.jenis_paket,
            jumlah_kalori=request.vars.jumlah_kalori,
            jumlah_paket_per_hari=request.vars.jumlah_paket_per_hari,
            tanggal_mulai=request.vars.tanggal_mulai,
            tanggal_selesai=request.vars.tanggal_selesai,
            durasi=(request.vars.tanggal_selesai - request.vars.tanggal_mulai).days 
               if request.vars.tanggal_mulai and request.vars.tanggal_selesai else None,
            total_biaya_kontrak=request.vars.total_biaya_kontrak,
            bukti_kontrak=request.vars.bukti_kontrak
        )
        # return dict(res='ok')
    

    
    return locals()

#------------------------------------------------------------------------------------
## untuk kepsek
#------------------------------------------------------------------------------------
@request.restful()
@cors_allow
def cek_kepsek():
    response.view = 'generic.json'
    
    def GET(t_id=None):
        sekolahan_saya = []
        id_sekolah=None
        nama_sekolah = 'Sekolah Debug'
        id_kelurahan_desa=0
        id_kode_pos=0
        id_user=None
        
        if t_id!=None:
            sekolahan_saya = db((db.map_sekolah_kepala.id_kepala_sekolah== db.auth_user.id) &
                (db.map_sekolah_kepala.id_sekolah==db.m_sekolah.id)& 
                (db.auth_user.id==t_id)
                ).select().as_list() 
        else:
           id_user=dict(id=2, first_name='Kepala', last_name='Sekolah') 

        if len(sekolahan_saya)==1:
            id_sekolah = sekolahan_saya[0]['m_sekolah']['id']
            nama_sekolah = sekolahan_saya[0]['m_sekolah']['nama_sekolah']
            id_kelurahan_desa=sekolahan_saya[0]['m_sekolah']['id_kelurahan_desa']
            id_kode_pos=sekolahan_saya[0]['m_sekolah']['id_kode_pos']
            id_user=dict(id=sekolahan_saya[0]['auth_user']['id'], first_name=sekolahan_saya[0]['auth_user']['first_name'], 
                last_name=sekolahan_saya[0]['auth_user']['last_name'])
            
        else:
            id_sekolah=1
            nama_sekolah = 'Sekolah Debug'
            id_kelurahan_desa=0
            id_kode_pos=0
            id_user=dict(id=2, first_name='Kepala', last_name='Sekolah') 

        return dict(id_sekolah=id_sekolah, nama_sekolah=nama_sekolah, id_kelurahan_desa =id_kelurahan_desa, 
            id_kode_pos=id_kode_pos, user=id_user)

    return locals()

def get_kepsek_id(t_id=None):
    # Fetch kepala sekolah data
    kepsek_data = db((db.map_sekolah_kepala.id_kepala_sekolah == db.auth_user.id) & 
                     (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id) & 
                     (db.auth_user.id == t_id)).select().first()
    
    if not kepsek_data:
        return dict(error="Kepsek not found")

    # Ensure id_kepsek is valid
    if not kepsek_data.m_sekolah.id:
        return dict(error="Invalid school ID for kepsek")

    id_kepsek = kepsek_data.m_sekolah.id
    return id_kepsek

@request.restful()
@cors_allow
def kepsek_paketku():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")

        try:
            t_id = int(request.vars.id_user)  # Ensure id_user is an integer
        except ValueError:
            return dict(error="Invalid id_user format. Must be an integer.")

        ids = get_kepsek_id(t_id)
        # Fetch kepala sekolah data
        kepsek_data = db((db.map_sekolah_kepala.id_kepala_sekolah == db.auth_user.id) & 
                         (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id) & 
                         (db.auth_user.id == t_id)).select().first()
        
        if not kepsek_data:
            return dict(error="Kepsek not found")

        # Ensure id_kepsek is valid
        if not kepsek_data.m_sekolah.id:
            return dict(error="Invalid school ID for kepsek")

        id_kepsek = kepsek_data.m_sekolah.id
        nama_sekolah = db(db.m_sekolah.id == id_kepsek).select().first().nama_sekolah

        paket_saya = db(
            (db.t_pemberian_paket.id_paket == db.m_paket.id) &
            (db.t_pemberian_paket.id_tujuan == kepsek_data.m_sekolah.id) &
            # (db.t_pemberian_paket.tanggal_pengiriman_dari_vendor != None) &
            (db.t_pemberian_paket.deleted == False)
        ).select().as_list()

        # Sanitizing response:
        for n in paket_saya:
            n['t_pemberian_paket'].pop('time_stamp', None)
            n['t_pemberian_paket'].pop('id_vendor', None)
            n['t_pemberian_paket'].pop('id_paket', None)
            n['m_paket'].pop('time_stamp', None)

        return dict(paket_saya=paket_saya, nama_sekolah=nama_sekolah, p=id_kepsek)

    def POST(*args, **vars):
        if request.vars.id_user==None:
            raise HTTP(400)
        if request.vars.id==None:
            raise HTTP(400)
        
        # Langsung ambil data vendor dari database, bukan dari API cek_vendor
        kepsek_data = db((db.map_sekolah_kepala.id_kepala_sekolah == db.auth_user.id) & 
                         (db.map_sekolah_kepala.id_sekolah == db.m_sekolah.id) & 
                         (db.auth_user.id == request.vars.id_user)).select().first()

        if not kepsek_data:
            return dict(error="Kepsek not found")

        id_kepsek = kepsek_data.m_sekolah.id
        qty = request.vars.qty
        ts = request.vars.waktu
        id = request.vars.id
        db.t_tanda_terima_paket.insert(id_t_pemberian_paket = id, jumlah = qty, 
            tanggal_terima = ts, id_user= id_kepsek)
        return dict(res='ok')
    return locals()

@request.restful()
@cors_allow
def data_siswa():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")

        try:
            t_id = int(request.vars.id_user)  # Ensure id_user is an integer
        except ValueError:
            return dict(error="Invalid id_user format. Must be an integer.")

        id_sekolah = get_kepsek_id(t_id)
        data_siswa = db((db.t_siswa.id_sekolah == id_sekolah)).select().as_list()
        return dict(data_siswa=data_siswa)

    def POST(*args, **vars):
        required_vars = ['id_user', 'nama', 'tanggal_lahir', 'jenis_kelamin', 'tempat_lahir']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_sekolah = get_kepsek_id(request.vars.id_user)
        db.t_siswa.insert(nama=request.vars.nama, id_sekolah=id_sekolah,
                        tanggal_lahir=request.vars.tanggal_lahir, 
                        jenis_kelamin = request.vars.jenis_kelamin, 
                        tempat_lahir = request.vars.tempat_lahir)
        id_record = db(db.t_siswa.nama == request.vars.nama).select().first().id
        return dict(res='ok', id_record=id_record)

    def PUT(*args, **vars):
        required_vars = ['id_user', 'id', 'nama', 'tanggal_lahir', 'jenis_kelamin', 'tempat_lahir']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        id_sekolah = get_kepsek_id(request.vars.id_user)
        db_now = db((db.t_siswa.id == request.vars.id) & (db.t_siswa.id_sekolah == id_sekolah))
        
        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.update(
            nama=request.vars.nama, tanggal_lahir=request.vars.tanggal_lahir, 
            jenis_kelamin = request.vars.jenis_kelamin, tempat_lahir = request.vars.tempat_lahir)
        id_record_updated = db_now.select().first().id
        return dict(res='ok', id_update=id_record_updated)

    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        id_sekolah = get_kepsek_id(request.vars.id_user)
        db_now = db((db.t_siswa.id == request.vars.id) & (db.t_siswa.id_sekolah == id_sekolah))
        
        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.delete()
        return dict(res='ok', id_deleted=request.vars.id)

    return locals()

@request.restful()
@cors_allow
def periksa_siswa():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")
        try:
            t_id = int(request.vars.id_user)  # Ensure id_user is an integer
        except ValueError:
            return dict(error="Invalid id_user format. Must be an integer.")
        id_sekolah = get_kepsek_id(t_id)
        data_siswa = db((db.t_siswa.id_sekolah == id_sekolah) & 
                (db.t_periksa_siswa.id_siswa == db.t_siswa.id)).select(db.t_periksa_siswa.ALL).as_list()
        return dict(data_siswa=data_siswa)

    def POST(*args, **vars):
        required_vars = ['id_user', 'id_siswa', 'berat_badan', 'tinggi_badan', 'tanggal_pengukuran']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_sekolah = get_kepsek_id(request.vars.id_user)
        if not db(db.t_siswa.id == request.vars.id_siswa).select().first():
            return dict(error="Siswa not found")

        db.t_periksa_siswa.insert(id_siswa=request.vars.id_siswa,
                                    berat_badan=request.vars.berat_badan,
                                  tinggi_badan=request.vars.tinggi_badan, 
                                  tangga_pengukuran=request.vars.tangga_pengukuran,)
        id_record = db(db.t_periksa_siswa.id_siswa == request.vars.id_siswa).select().last().id
        return dict(res='ok', id_record = id_record)

    def PUT(*args, **vars):
        required_vars = ['id_user', 'id', 'berat_badan', 'tinggi_badan', 'tanggal_pengukuran']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        db_now = db((db.t_periksa_siswa.id == request.vars.id) & 
                    (db.t_periksa_siswa.id_siswa == db.t_siswa.id)).select().first()
        
        if not db_now:
            return dict(error="Record not found")
        
        db_now.update(berat_badan=request.vars.berat_badan, tinggi_badan=request.vars.tinggi_badan, 
                      tanggal_pengukuran=request.vars.tanggal_pengukuran)
        id_record_updated = db_now.t_periksa_siswa.id
        return dict(res='ok', id_update=id_record_updated)

    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        db_now = db((db.t_periksa_siswa.id == request.vars.id) & 
                    (db.t_periksa_siswa.id_siswa == db.t_siswa.id)).select().first()
        
        if not db_now:
            return dict(error="Record not found")
        
        db(db.t_periksa_siswa.id == request.vars.id).delete()
        return dict(res='ok', id_deleted=request.vars.id)
    return locals()

#------------------------------------------------------------------------------------
## untuk Vendor
#------------------------------------------------------------------------------------

# CEK VENDOR
@request.restful()
@cors_allow
def cek_vendor():
    response.view = 'generic.json'
    
    def GET(id_user=None):
        vendor_saya1 = []
        id_vendor = None
        nama_vendor = 'Vendor Debug'

        # Ambil id_user dari request.vars (misal: ?id_user=3)
        t_id = request.vars.id_user 
        
        if t_id:
            try:
                t_id = int(t_id)  # Pastikan id_user adalah integer
                vendor_saya1 = db((db.map_vendor_user.id_user == db.auth_user.id) & 
                                  (db.map_vendor_user.id_vendor == db.m_vendor.id) & 
                                  (db.auth_user.id == t_id)).select().as_list()
            except ValueError:
                return dict(error="Invalid id format")

        else:
            return dict(error="id_user is required")

        if len(vendor_saya1) == 1:
            id_vendor = vendor_saya1[0]['m_vendor']['id']
            nama_vendor = vendor_saya1[0]['m_vendor']['nama_vendor']
            id_kelurahan_desa = vendor_saya1[0]['m_vendor']['id_kelurahan_desa']
            id_kode_pos = vendor_saya1[0]['m_vendor']['id_kode_pos']
            id_user = dict(id=vendor_saya1[0]['auth_user']['id'], 
                           first_name=vendor_saya1[0]['auth_user']['first_name'], 
                           last_name=vendor_saya1[0]['auth_user']['last_name'])
        else:
            return dict(error="Vendor not found")

        return dict(id_vendor=id_vendor, nama_vendor=nama_vendor, 
                    id_kelurahan_desa=id_kelurahan_desa, id_kode_pos=id_kode_pos, user=id_user)

    return locals()

def get_vendor_id(t_id=None):
    #Langsung ambil data vendor dari database, bukan dari API cek_vendor
    vendor_data = db((db.map_vendor_user.id_user == db.auth_user.id) & 
                    (db.map_vendor_user.id_vendor == db.m_vendor.id) & 
                    (db.auth_user.id == t_id)).select().first()

    if not vendor_data:
       return dict(error="Vendor not found")

    id_vendor = vendor_data.m_vendor.id
    return id_vendor

# VENDOR ORDERKU
@request.restful()
@cors_allow
def vendor_orderku():
    response.view = 'generic.json'
    def GET(id_user=None):
        if not request.vars.id_user:
            return dict(error="id_user is required")       
        try:
            t_id = int(request.vars.id_user)
        except ValueError:
            return dict(error="Invalid id format")

        id_vendor = get_vendor_id(request.vars.id_user)

        q = ((db.t_pemberian_paket.id_vendor == id_vendor) &
            (db.t_pemberian_paket.tanggal_pengiriman_dari_vendor == None) &
            (db.t_pemberian_paket.id_tujuan == db.m_sekolah.id) &
            (db.t_pemberian_paket.id_paket == db.m_paket.id))
        
        l = db(q).select().as_list()

        # Sanitizing response
        for n in l:
            n['t_pemberian_paket'].pop('time_stamp', None)
            n['t_pemberian_paket'].pop('id_vendor', None)
            n['t_pemberian_paket'].pop('id_paket', None)
            n['m_paket'].pop('time_stamp', None)
            n['m_sekolah'].pop('time_stamp', None)

        return dict(orderku=l)

    return locals()

# VENDOR Konfirmasi Pengiriman Paket
@request.restful()
@cors_allow
def vendor_jumlah():
    response.view = 'generic.json'
    def PUT(*args, **vars):
        if request.vars.id_user==None:
            raise HTTP(400)        
        if request.vars.id==None:
            raise HTTP(400) 

        id_vendor = get_vendor_id(request.vars.id_user)
        db((db.t_pemberian_paket.id==request.vars.id) & 
           (db.t_pemberian_paket.id_vendor == id_vendor)).update(tanggal_pengiriman_dari_vendor=request.vars.tanggal, 
            jumlah_dari_vendor=request.vars.qty, id_user=request.vars.id_user)
        return dict(res='ok', id_vendor=id_vendor)
    return locals()

@request.restful()
@cors_allow
def vendor_orderku_total():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if request.vars.id_user==None:
            raise HTTP(400)        

        id_vendor = get_vendor_id(request.vars.id_user)

        q = ((db.t_pemberian_paket.id_vendor == id_vendor) &
            (db.t_pemberian_paket.id_tujuan == db.m_sekolah.id) &
            (db.t_pemberian_paket.id_paket == db.m_paket.id))
        l = db(q).select().as_list()
        #sanitizing response:
        for n in l:
            n['t_pemberian_paket'].pop('time_stamp')
            n['t_pemberian_paket'].pop('id_vendor')
            n['t_pemberian_paket'].pop('id_paket')
            n['m_paket'].pop('time_stamp')
            n['m_sekolah'].pop('time_stamp')

        return dict(orderku=l)
    return locals()

#Tambah Produk Vendor
@request.restful()
@cors_allow
def vendor_paket():
    response.view = 'generic.json'
    def GET(*args, **vars):
        response.view = 'generic.json'
        if not request.vars.id_user:
            return dict(error="id_user is required")
        try:
            t_id = int(request.vars.id_user)
        except ValueError:
            return dict(error="Invalid id format")
        
        id_vendor = get_vendor_id(request.vars.id_user)
       
        q = db(db.m_paket.id_vendor == id_vendor).select().as_list()
        #sanitizing response:
        for n in q:
            n.pop('time_stamp')
            n.pop('deleted')
        return dict(daftar=q)
    
    def POST(*args, **vars):
        required_vars = ['id_user', 'nama_paket', 'pagu_harga', 'kalori']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_vendor = get_vendor_id(request.vars.id_user)
        if not db(db.m_paket.nama_paket == request.vars.nama_paket).select().first():
            db.m_paket.insert(id_vendor=id_vendor, nama_paket=request.vars.nama_paket, 
                              pagu_harga=request.vars.pagu_harga, kalori=request.vars.kalori)
        else:
            return dict(error="Product already exists")

        return dict(res='ok')

    def PUT(*args, **vars):
        required_vars = ['id_user', 'id_paket', 'nama_paket', 'pagu_harga', 'kalori']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_vendor = get_vendor_id(request.vars.id_user)
        db_now = db((db.m_paket.id == request.vars.id_paket) & (db.m_paket.id_vendor == id_vendor))
        
        if not db_now.select().first():
            return dict(error="Product not found")
        
        db_now.update(nama_paket=request.vars.nama_paket, pagu_harga=request.vars.pagu_harga, 
                      kalori=request.vars.kalori)
        id_record_updated = db_now.select().first().id
        return dict(res='ok', id_update=id_record_updated)

    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id_paket']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_vendor = get_vendor_id(request.vars.id_user)
        db_now = db((db.m_paket.id == request.vars.id_paket) & (db.m_paket.id_vendor == id_vendor))
        
        if not db_now.select().first():
            return dict(error="Product not found")
        
        db_now.delete()
        return dict(res='ok', id_deleted=request.vars.id_paket)
    return locals()

@request.restful()
@cors_allow
def vendor_pesan_supplier():
    response.view = 'generic.json'

    def GET(*args, **vars):   
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")
        # Langsung ambil data vendor dari database, bukan dari API cek_vendor
        supplier_data = db((db.map_supplier_user.id_user == db.auth_user.id) & 
                         (db.map_supplier_user.id_supplier == db.m_supplier.id) & 
                         (db.auth_user.id == request.vars.id_user)).select().first()
        if not supplier_data:
            return dict(error="Supplier not found")
        
        id_supplier = supplier_data.m_supplier.id
        
        #cari alamat:
        pesanan_supplier = db((db.t_pembelian_bahan.id_supplier==id_supplier)).select().first()
        return dict(stok=pesanan_supplier)

    def POST(*args, **vars):
        required_vars = ['id_user', 'id_supplier', 'nama_item', 'volume']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        vendor_data = db((db.map_vendor_user.id_user == db.auth_user.id) & 
                    (db.map_vendor_user.id_vendor == db.m_vendor.id) & 
                    (db.auth_user.id == request.vars.id_user)).select().first()

        if not vendor_data:
            return dict(error="Vendor not found")

        nama_vendor = vendor_data.m_vendor.nama_vendor
        
        id_vendor = get_vendor_id(request.vars.id_user)

        item = db((db.t_harga_supplier.nama_item == request.vars.nama_item)).select().first()
        harga_item = item.harga
        satuan_item = db((db.m_satuan_supplier.id == item.id_satuan_supplier)).select().first().nama_satuan
        id_satuan_supplier = item.id_satuan_supplier

        db.t_pembelian_bahan.insert(id_vendor=id_vendor, id_supplier=request.vars.id_supplier, 
                                    nama_vendor = nama_vendor, harga = harga_item, id_satuan_supplier = id_satuan_supplier,
                                    nama_item = request.vars.nama_item, volume=request.vars.volume)
        return dict(res='ok')
    
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id_supplier', 'id_item', 'volume', 'nama_item', 'sudah_diterima']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        vendor_data = db((db.map_vendor_user.id_user == db.auth_user.id) & 
                    (db.map_vendor_user.id_vendor == db.m_vendor.id) & 
                    (db.auth_user.id == request.vars.id_user)).select().first()

        if not vendor_data:
            return dict(error="Vendor not found")

        id_vendor = get_vendor_id(request.vars.id_user)
        db((db.t_pembelian_bahan.id == request.vars.id_item) & 
           (db.t_pembelian_bahan.id_vendor == id_vendor)).update(
                                volume=request.vars.volume, 
                                nama_item=request.vars.nama_item,
                                sudah_diterima = request.vars.sudah_diterima)  
        return dict(res='ok')

    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id_item']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        vendor_data = db((db.map_vendor_user.id_user == db.auth_user.id) & 
                    (db.map_vendor_user.id_vendor == db.m_vendor.id) & 
                    (db.auth_user.id == request.vars.id_user)).select().first()

        if not vendor_data:
            return dict(error="Vendor not found")

        id_vendor = get_vendor_id(request.vars.id_user)
        db((db.t_pembelian_bahan.id == request.vars.id_item) & 
           (db.t_pembelian_bahan.id_vendor == id_vendor)).update(deleted = True)
        return dict(res='ok')

    return locals()
    

#------------------------------------------------------------------------------------
## untuk Supplier
#------------------------------------------------------------------------------------

@request.restful()
@cors_allow
def cek_suppliers():
    response.view = 'generic.json'
    def GET(*args, **vars):
        id_toko_saya=[]
        if request.vars.id_user != None:
            id_toko_saya = db((db.m_supplier.id==db.map_supplier_user.id_supplier)&
                            (db.map_supplier_user.id_user==request.vars.id_user)).select().as_list()
            
        daftar_barang=[]
        nama_supplier='-'
        id=None
        id_kelurahan_desa=0
        id_kode_pos=0
        if len(id_toko_saya)==1:
            id = id_toko_saya[0]['m_supplier']['id']
            nama_supplier = id_toko_saya[0]['m_supplier']['nama_supplier']
            id_kelurahan_desa=id_toko_saya[0]['m_supplier']['id_kelurahan_desa']
            id_kode_pos=id_toko_saya[0]['m_supplier']['id_kode_pos']
        else: #debug tanpa login
            id = 1
            nama_supplier = 'Depot Sayur Debug'
            id_kelurahan_desa=0
            id_kode_pos=0

        return dict(supplier=id_toko_saya)
    return locals()

@request.restful()
@cors_allow
def stok_item_supplier():
    
    response.view = 'generic.json'
    def GET(*args, **vars):
        
        t_id = request.vars.id_user
        #Langsung ambil data vendor dari database, bukan dari API cek_vendor
        if t_id:
            supplier_data = db((db.map_supplier_user.id_user == db.auth_user.id) & 
                         (db.map_supplier_user.id_supplier == db.m_supplier.id) & 
                         (db.auth_user.id == t_id)).select().first()
            if not supplier_data:
                return dict(error="Supplier not found")

            id_supplier = supplier_data.m_supplier.id

            q = db( (db.t_harga_supplier.id_supplier == id_supplier)&
                    (db.t_harga_supplier.id_satuan_supplier == db.m_satuan_supplier.id)        
                    ).select().as_list()
        else:
            q = db.t_harga_supplier.select().as_list()
        
        #sanitizing response:    
        for w in q:
            w['t_harga_supplier'].pop('time_stamp')
            w['t_harga_supplier'].pop('id_supplier')
            w['t_harga_supplier']['satuan']=w['m_satuan_supplier']['nama_satuan']
            w['t_harga_supplier'].pop('id_satuan_supplier')
            w.pop('m_satuan_supplier')

        return dict(daftar=q)

    return locals()    

@request.restful()
@cors_allow
def tambah_stok_item_supplier():    
    response.view = 'generic.json'
    def PUT(*args, **vars):
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")
        if not request.vars.id_stok:
            raise HTTP(400, "Missing id_stok")
        

        t_id = request.vars.id_user
        #Langsung ambil data vendor dari database, bukan dari API cek_vendor
        supplier_data = db((db.map_supplier_user.id_user == db.auth_user.id) & 
                         (db.map_supplier_user.id_supplier == db.m_supplier.id) & 
                         (db.auth_user.id == t_id)).select().first()
        if not supplier_data:
            return dict(error="Supplier not found")

        id_supplier = supplier_data.m_supplier.id
    
        db((db.t_harga_supplier.id == request.vars.id_stok) &
        (db.t_harga_supplier.id_supplier == id_supplier)
        ).update(volume=request.vars.qty)
        return dict(res='ok', id_supplier=id_supplier, updated_item_id = request.vars.id_stok)

    return locals()

@request.restful()
@cors_allow
def tambah_item_baru_supplier():
    response.view = 'generic.json'

    #GET Nama Satuan Item
    def GET(*args, **vars):
        daftar_satuan = db(db.m_satuan_supplier["nama_satuan"]).select().as_list()

        if request.vars.satuan != daftar_satuan[2]:
            db.m_satuan_supplier.insert(nama_satuan=request.vars.satuan)
            daftar_satuan = db(db.m_satuan_supplier).select().as_list()
        return dict(daftar_satuan = daftar_satuan)
    #POST Item satuan
    def POST(*args, **vars):
        if not (request.vars.id_user and request.vars.nama_item and request.vars.qty and request.vars.harga):
            raise HTTP(400, "Missing required parameters")

        t_id = request.vars.id_user
        #Langsung ambil data vendor dari database, bukan dari API cek_vendor
        supplier_data = db((db.map_supplier_user.id_user == db.auth_user.id) & 
                         (db.map_supplier_user.id_supplier == db.m_supplier.id) & 
                         (db.auth_user.id == t_id)).select().first()
        if not supplier_data:
            return dict(error="Supplier not found")

        id_supplier = supplier_data.m_supplier.id

        
        daftar_satuan = db(db.m_satuan_supplier["nama_satuan"]).select().as_list()
        nama_satuan_list = [item["nama_satuan"] for item in daftar_satuan]
        
        if request.vars.satuan != nama_satuan_list:
            db.m_satuan_supplier.insert(nama_satuan=request.vars.satuan)
            daftar_satuan = db(db.m_satuan_supplier).select().as_list()

        id_satuan = db(db.m_satuan_supplier["nama_satuan"] == request.vars.satuan).select().as_list()[0]['id']

        db.t_harga_supplier.insert(id_supplier= id_supplier, 
                                   nama_item=request.vars.nama_item, 
                                   volume=request.vars.qty, 
                                   harga=request.vars.harga,
                                   id_satuan_supplier=id_satuan)
        return dict(res='ok')

    return locals()


#------------------------------------------------------------------------------------
## untuk Watchdog
#------------------------------------------------------------------------------------

@request.restful()
@cors_allow
def keluhan_user():
    response.view = 'generic.json'

    #GET ALL Response
    def GET(*args, **vars):
        keluhan = db(db.t_keluhan_user).select().as_list()
        return dict(res=keluhan)

    def POST(*args, **vars):
        if not (request.vars.keluhan):
            raise HTTP(400, "Missing required parameters")

        db.t_keluhan_user.insert(id_user=request.vars.id_user, keluhan=request.vars.keluhan)
        return dict(res='ok')    

    def DELETE(*args, **vars):
        if not request.vars.id_keluhan:
            raise HTTP(400, "Missing required parameters")

        db(db.t_keluhan_user.id == request.vars.id_keluhan).update(deleted=True)
        return dict(res='ok') 
    return locals()