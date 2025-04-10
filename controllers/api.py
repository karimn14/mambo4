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

# @request.restful()
# @cors_allow
# def login():
#     response.view = 'generic.json'
#     def POST(*args, **vars):
#         email = request.vars.email
#         password = request.vars.password
#         user = authenticate_user(email, password)
#         if not user:
#             return dict(error="Incorrect email or password")
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(
#             data={"sub": user.username}, expires_delta=access_token_expires
#         )
#         return dict(access_token=access_token, token_type="bearer")
#     return locals()

#------------------------------------------------------------------------------------
## barre login
@request.restful()
@cors_allow
def bare_login():
    response.view = 'generic.json'
    def GET(*args, **vars):        
        u_name = request.vars.u
        pw = request.vars.pw
        test = auth.login_bare(u_name, pw)
        if test != False:
            # Sanitize data
            role = db((db.auth_membership.user_id == test['id']) &
                      (db.auth_membership.group_id == db.auth_group.id)).select().as_list()
            test.pop('password')
            test.pop('reset_password_key')
            test.pop('registration_key')
            test.pop('registration_id')
            test['role'] = role[0]['auth_group']['role']
            response.status = 200
            return dict(status="success", message="Login successful", data=test)
        else:
            response.status = 401
            return dict(status="fail", message="Invalid username or password")
    return locals()

@request.restful()
@cors_allow
def reset_password():
    response.view = 'generic.json'
    def POST(*args, **vars):
        required_vars = ['email', 'new_password']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        email = request.vars.email
        new_password = request.vars.new_password
        # Fetch user by email
        user = db(db.auth_user.email == email).select().first()
        if not user:
            return dict(error="User not found")
        # Update password
        hashed_password = db.auth_user.password.validate(new_password)[0]
        user.update_record(password=hashed_password)
        db.commit()
        return dict(res="Password reset successful")
    return locals()

#------------------------------------------------------------------------------------
## untuk semua akun
#------------------------------------------------------------------------------------

@request.restful()
@cors_allow
def status_paket():
    response.view = 'generic.json'
    def GET(*args, **vars):
        response.view = 'generic.json'
        
        status_paket = db(db.t_status_paket).select().as_list()
        return dict(status_paket=status_paket)
    return locals()

#------------------------------------------------------------------------------------
## untuk master admin
#------------------------------------------------------------------------------------

@request.restful()
@cors_allow
def data_sekolah():
    response.view = 'generic.json'

    def GET(*args, **vars):
        # Fetch all schools or a specific school by ID
        if request.vars.id:
            try:
                school_id = int(request.vars.id)
                school = db(db.m_sekolah.id == school_id).select().first()
                if not school:
                    return dict(error="School not found")
                return dict(school=school.as_dict())
            except ValueError:
                return dict(error="Invalid school ID format")
        else:
            schools = db(db.m_sekolah).select().as_list()
            return dict(schools=schools)

    def POST(*args, **vars):
        # Add a new school
        required_vars = ['nama_sekolah', 'alamat', 'id_kelurahan_desa', 'id_kode_pos']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        new_school_id = db.m_sekolah.insert(
            nama_sekolah=request.vars.nama_sekolah,
            alamat=request.vars.alamat,
            id_kelurahan_desa=request.vars.id_kelurahan_desa,
            id_kode_pos=request.vars.id_kode_pos
        )
        return dict(res='ok', id=new_school_id)

    def PUT(*args, **vars):
        # Update an existing school
        required_vars = ['id', 'nama_sekolah', 'alamat', 'id_kelurahan_desa', 'id_kode_pos']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        try:
            school_id = int(request.vars.id)
        except ValueError:
            return dict(error="Invalid school ID format")

        db_now = db(db.m_sekolah.id == school_id)
        if not db_now.select().first():
            return dict(error="School not found")

        db_now.update(
            nama_sekolah=request.vars.nama_sekolah,
            alamat=request.vars.alamat,
            id_kelurahan_desa=request.vars.id_kelurahan_desa,
            id_kode_pos=request.vars.id_kode_pos
        )
        return dict(res='ok', id_update=school_id)

    def DELETE(*args, **vars):
        # Delete a school
        if not request.vars.id:
            raise HTTP(400, "Missing school ID")

        try:
            school_id = int(request.vars.id)
        except ValueError:
            return dict(error="Invalid school ID format")

        db_now = db(db.m_sekolah.id == school_id)
        if not db_now.select().first():
            return dict(error="School not found")

        db_now.delete()
        return dict(res='ok', id_deleted=school_id)

    return locals()

#------------------------------------------------------------------------------------
## untuk disdik
#------------------------------------------------------------------------------------

#disdik auth_user.id_user=3
def get_disdik_id(t_id=None):
    # Fetch disdik data
    disdik_data = db((db.map_admin_disdik.id_admin == t_id)).select().first()
    
    if not disdik_data:
        raise ValueError("Disdik not found or invalid Disdik ID")

    return disdik_data.id_disdik

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
        db_now = db(db.t_kontrak_disdik).select().as_list()
        return dict(kontrak=db_now)

    def POST(*args, **vars):
        required_vars = ['id_user', 'id_vendor', 'nama', 'nip_npwp', 'jabatan', 
                         'alamat_vendor', 'instansi', 'jenis_paket', 'jumlah_kalori', 
                         'jumlah_paket_per_hari', 'tanggal_mulai', 'tanggal_selesai', 
                         'total_biaya_kontrak', 'bukti_kontrak']
        missing_vars = []
        for var in required_vars:
            if var == 'bukti_kontrak':
                value = request.vars.get(var)
                # Instead of using "if not value", check explicitly for None and filename
                if value is None:
                    missing_vars.append(var)
                elif not hasattr(value, 'filename'):
                    missing_vars.append(var)
                else:
                    filename = value.filename
                    if filename is None or filename.strip() == "":
                        missing_vars.append(var)
            else:
                value = request.vars.get(var)
                if value is None or (isinstance(value, str) and value.strip() == ''):
                    missing_vars.append(var)
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        try:
            id_disdik = get_disdik_id(request.vars.id_user)
        except ValueError as e:
            raise HTTP(400, str(e))

        # Convert date strings to date objects.
        from datetime import datetime
        try:
            tanggal_mulai = datetime.strptime(request.vars.tanggal_mulai, '%Y-%m-%d').date()
            tanggal_selesai = datetime.strptime(request.vars.tanggal_selesai, '%Y-%m-%d').date()
        except Exception as e:
            raise HTTP(400, f"Invalid date format: {e}")

        # Calculate duration (durasi) in days.
        durasi = (tanggal_selesai - tanggal_mulai).days if tanggal_mulai and tanggal_selesai else None

        db.t_kontrak_disdik.insert(
            id_disdik=id_disdik,
            id_vendor=request.vars.id_vendor,
            id_sekolah=request.vars.id_sekolah,
            id_paket=request.vars.id_paket,
            nama=request.vars.nama,
            nip_npwp=request.vars.nip_npwp,
            jabatan=request.vars.jabatan,
            alamat=request.vars.alamat_vendor,
            instansi=request.vars.instansi,
            jenis_paket=request.vars.jenis_paket,
            jumlah_kalori=request.vars.jumlah_kalori,
            jumlah_paket_per_hari=request.vars.jumlah_paket_per_hari,
            tanggal_mulai=tanggal_mulai,
            tanggal_selesai=tanggal_selesai,
            durasi=durasi,
            total_biaya_kontrak=request.vars.total_biaya_kontrak,
            bukti_kontrak=request.vars.bukti_kontrak
        )
        return dict(res='ok')
    
    return locals()

#debug
@request.restful()
@cors_allow
def pengajuan_paket():
    response.view = 'generic.json'
    
    def GET(*args, **vars):
        # Build a query to fetch non-deleted records
        query = (db.t_pengajuan_paket.deleted == False)
        # Optional filtering: if id_vendor is provided, filter by it.
        if request.vars.id_vendor:
            query &= (db.t_pengajuan_paket.id_vendor == request.vars.id_vendor)
        records = db(query).select().as_list()
        return dict(pengajuan_paket=records)
    
    def POST(*args, **vars):
        # Required fields for insertion
        required_vars = ['id_vendor', 'id_disdik', 'id_sekolah', 'id_paket', 'jumlah', 'jenis_paket']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        # Insert the new record into t_pengajuan_paket.
        new_id = db.t_pengajuan_paket.insert(
            id_vendor = request.vars.id_vendor,
            id_disdik = request.vars.id_disdik,
            id_sekolah = request.vars.id_sekolah,
            id_paket = request.vars.id_paket,
            jumlah = int(request.vars.jumlah),
            jenis_paket = request.vars.jenis_paket,
            approve = False,
            time_stamp_setuju = None,
            time_stamp = request.now,
            deleted = False
        )
        db.commit()
        return dict(res='ok', id=new_id)
    
    return locals()

#------------------------------------------------------------------------------------
## untuk kepsek
#------------------------------------------------------------------------------------

def get_kepsek_id(t_id=None):
    # Fetch kepala sekolah data
    kepsek_data = db(db.map_sekolah_kepala.id_kepala_sekolah == t_id).select().first()
    
    if not kepsek_data:
        return "Tidak ditemukan sekolah kepsek"  # Return None if no data is found

    # Return only the id_sekolah value
    return kepsek_data.id_sekolah

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
            (db.t_status_paket.id_sekolah == kepsek_data.m_sekolah.id) &
            (db.t_status_paket.deleted == False)
        ).select().as_list()

        # Sanitizing response:
        for n in paket_saya:
            n['t_status_paket'].pop('time_stamp', None)
            n['t_status_paket'].pop('deleted', None)

        return dict(paket_saya=paket_saya, nama_sekolah=nama_sekolah, id_kepsek=id_kepsek)
    
    def PUT(*args, **vars):
        required_vars = ['id_t_pengajuan_paket', 'id_kepsek']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        id_t_pengajuan_paket = request.vars.id_t_pengajuan_paket
        id_kepsek = request.vars.id_kepsek
        db_now = db((db.t_status_paket.id_t_pengajuan_paket == id_t_pengajuan_paket) & 
                    (db.t_status_paket.id_kepsek == id_kepsek))
        
        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.update(status="Sudah Diterima")
        return dict(res='ok', id_update=id_t_pengajuan_paket)
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
        if not request.vars.id_sekolah:
            raise HTTP(400, "Missing id_sekolah")
        try:
            t_id = int(request.vars.id_sekolah)  # Ensure id_sekolah is an integer
        except ValueError:
            return dict(error="Invalid id_sekolah format. Must be an integer.")
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
                                  tinggi_badan = request.vars.tinggi_badan, 
                                  tanggal_pengukuran=request.vars.tanggal_pengukuran,)
        id_record = db(db.t_periksa_siswa.id_siswa == request.vars.id_siswa).select().last().id
        return dict(res='ok', id_record = id_record)

    def PUT(*args, **vars):
        required_vars = ['id', 'berat_badan', 'tinggi_badan', 'tanggal_pengukuran']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        db_now = db((db.t_periksa_siswa.id == request.vars.id))

        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.update(berat_badan=request.vars.berat_badan, tinggi_badan=request.vars.tinggi_badan, 
                      tanggal_pengukuran=request.vars.tanggal_pengukuran)
        id_record_updated = db_now.select().first().id
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

@request.restful()
@cors_allow
def pesanan_sekolah():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if not request.vars.id_sekolah:
            raise HTTP(400, "Missing id_sekolah")
        try:
            id_sekolah = int(request.vars.id_sekolah)  # Ensure id_sekolah is an integer
        except ValueError:
            return dict(error="Invalid id_sekolah format. Must be an integer.")
        
        pesanan = db(db.t_status_paket.id_sekolah == id_sekolah).select().as_list()
        
        # Sanitize response
        sanitized_pesanan = []
        for p in pesanan:
            sanitized_pesanan.append({
                'status': p['status'],
                'id_sekolah': p['id_sekolah'],
                'id_paket': p['id_paket'],
                'id_vendor': p['id_vendor']
            })
        
        return dict(pesanan=sanitized_pesanan)
    return locals()

@request.restful()
@cors_allow
def terima_paket():
    response.view = 'generic.json'
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id', 'id_vendor']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_sekolah = get_kepsek_id(request.vars.id_user)
        
        db_now = db((db.t_status_paket.id_sekolah == id_sekolah) & 
                    (db.t_status_paket.id_t_pengajuan_paket == request.vars.id) & 
                    (db.t_status_paket.id_vendor == request.vars.id_vendor))
        
        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.update(status="Diterima", ts_diterima=request.now)
        
        return dict(res='ok', id_update=request.vars.id)
    return locals()


#------------------------------------------------------------------------------------
## untuk Vendor
#------------------------------------------------------------------------------------

# CEK VENDOR
def get_vendor_id(t_id=None):
    # Fetch vendor data from the database
    vendor_data = db((db.map_vendor_user.id_user == t_id)).select().first()

    if not vendor_data:
        return "Vendor not found"  # Raise an error if vendor is not found

    return vendor_data.id_vendor  # Return the vendor ID as an integer

def get_vendor(t_id=None):
    # Fetch vendor data from the database\
    id_vendor = get_vendor_id(t_id)
    vendor_data = db((db.m_vendor.id == id_vendor)).select().first()
    
    if not vendor_data:
        return "Vendor not found"  # Raise an error if vendor is not found

    return vendor_data

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

# Menu Vendor
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
            
        id_vendor = int(get_vendor_id(request.vars.id_user))
        if not isinstance(id_vendor, int):
            raise HTTP(400, "Invalid id_vendor format. Must be an integer.")
        
        # Validate data types and constraints
        try:
            pagu_harga = float(request.vars.pagu_harga)
            kalori = float(request.vars.kalori)
        except ValueError:
            raise HTTP(400, "Invalid data type for 'pagu_harga' or 'kalori'")
        
        if not db(db.m_paket.nama_paket == request.vars.nama_paket).select().first():
            db.m_paket.insert(
                id_vendor=id_vendor,
                nama_paket=request.vars.nama_paket,
                pagu_harga=pagu_harga,
                kalori=kalori
            )
        else:
            return dict(error="Product already exists")
        db.commit()
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
        pesanan_supplier = db((db.t_pembelian_bahan.id_supplier==id_supplier)).select()
        return dict(stok=pesanan_supplier)

    def POST(*args, **vars):
        required_vars = ['id_user', 'id_supplier', 'nama_item', 'volume']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_vendor = get_vendor_id(request.vars.id_user)
        nama_vendor = (get_vendor(request.vars.id_user)).nama_vendor
        item = db((db.t_menu_supplier.nama_item == request.vars.nama_item)).select().first()
        
        if not item:
            return dict(error="Item not available")
        else:
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
    
@request.restful()
@cors_allow
def status_paket_vendor():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if request.vars.id_user:
            try:
                t_id = int(request.vars.id_user)
            except ValueError:
                return dict(error="Invalid id format")
            
            id_vendor = get_vendor_id(request.vars.id_user)
            q = db(db.t_status_paket.id_vendor == id_vendor).select().as_list()
        else:
            q = db(db.t_status_paket).select().as_list()
        
        return dict(status_paket=q)
    return locals()

@request.restful()
@cors_allow
def kirim_paket():
    response.view = 'generic.json'
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id', 'id_sekolah']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_vendor = get_vendor_id(request.vars.id_user)
        db_now = db((db.t_status_paket.id_vendor == id_vendor) & 
                    (db.t_status_paket.id_t_pengajuan_paket == request.vars.id) & 
                    (db.t_status_paket.id_sekolah == request.vars.id_sekolah))
        
        if not db_now.select().first():
            return dict(error="Record not found")
        
        db_now.update(status="Dikirim", ts_dikirim=request.now)
        return dict(res=f"{request.vars.id} sudah terkirim")
    
    return locals()

@request.restful()
@cors_allow
def terima_pengajuan():
    response.view = 'generic.json'
    
    def PUT(*args, **vars):
        # Required fields for update
        required_vars = ['id', 'approve', 'id_vendor']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        # Update the record in t_pengajuan_paket.
        db_now = db((db.t_pengajuan_paket.id == request.vars.id) & 
                (db.t_pengajuan_paket.id_vendor == request.vars.id_vendor))
        if not db_now.select().first():
            return dict(error="Record not found")

        # Update the record in t_status_paket.
        db_now2 = db((db.t_status_paket.id_t_pengajuan_paket == request.vars.id) & 
                 (db.t_status_paket.id_vendor == request.vars.id_vendor))
        if not db_now2.select().first():
            return dict(error="Record not found in Status Paket Table")
        
        if request.vars.approve:
            db_now2.update(status="Diproses", ts_diproses_ditolak=request.now)
        else:
            db_now2.update(status="Ditolak", ts_diproses_ditolak=request.now)

        db_now.update(approve=bool(request.vars.approve), id_vendor=request.vars.id_vendor, time_stamp_update=request.now)
        return dict(res='ok', id=request.vars.id)
    return locals()

#------------------------------------------------------------------------------------
## untuk Supplier
#------------------------------------------------------------------------------------

#id_user : 4 for id_supplier : 1
#id_user : 7 for id_supplier : 2
def get_supplier_id(t_id=None):
    #Langsung ambil data vendor dari database, bukan dari API cek_vendor
    supplier_data = db((db.map_supplier_user.id_user == t_id)).select().first()

    if not supplier_data:
       return dict(error="Supplier not found")

    id_supplier = supplier_data.id_supplier
    return id_supplier

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
def menu_supplier():
    response.view = 'generic.json'
    
    def GET(*args, **vars):

        if request.vars.id_user:
            id_supplier = get_supplier_id(request.vars.id_user)
            q = db(db.t_menu_supplier.id_supplier == id_supplier).select().as_list()
        else:
            q = db(db.t_menu_supplier).select().as_list()
        # Sanitizing response
        for item in q:
            item.pop('time_stamp', None)
            item.pop('id_supplier', None)
        
        return dict(daftar=q)
    
    def POST(*args, **vars):
        required_vars = ['id_user', 'nama_item', 'harga', 'volume', 'id_satuan_supplier']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db.t_menu_supplier.insert(
            id_supplier=id_supplier,
            nama_item=request.vars.nama_item,
            harga=request.vars.harga,
            volume=request.vars.volume,
            id_satuan_supplier=request.vars.id_satuan_supplier
        )
        return dict(res='ok')
        
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id_item', 'nama_item', 'harga', 'volume', 'id_satuan_supplier']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db_now = db((db.t_menu_supplier.id == request.vars.id_item) & (db.t_menu_supplier.id_supplier == id_supplier))
        
        if not db_now.select().first():
            return dict(error="Item not found")
        
        db_now.update(
            nama_item=request.vars.nama_item,
            harga=request.vars.harga,
            volume=request.vars.volume,
            id_satuan_supplier=request.vars.id_satuan_supplier
        )
        return dict(res='ok', id_update=request.vars.id_item)
        
    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id_item']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db_now = db((db.t_menu_supplier.id == request.vars.id_item) & (db.t_menu_supplier.id_supplier == id_supplier))
        
        if not db_now.select().first():
            return dict(error="Item not found")
        
        db_now.update(deleted=True)
        return dict(res='ok', id_deleted=request.vars.id_item)
        
    return locals()
    
@request.restful()
@cors_allow
def pesanan_vendor():
    response.view = 'generic.json'
    def GET(*args, **vars):
        if not request.vars.id_user:
            raise HTTP(400, "Missing id_user")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        pesanan = db(db.t_pembelian_bahan.id_supplier == id_supplier).select().as_list()
        
        # Sanitize response
        for p in pesanan:
            p.pop('time_stamp', None)
            p.pop('deleted', None)
        
        return dict(pesanan=pesanan)
    
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id_item', 'volume', 'nama_item', 'sudah_diterima']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db_now = db((db.t_pembelian_bahan.id == request.vars.id_item) & 
                    (db.t_pembelian_bahan.id_supplier == id_supplier))
        
        if not db_now.select().first():
            return dict(error="Item not found")
        
        db_now.update(
            volume=request.vars.volume,
            nama_item=request.vars.nama_item,
            sudah_diterima=request.vars.sudah_diterima
        )
        return dict(res='ok', id_update=request.vars.id_item)
        
    def DELETE(*args, **vars):
        required_vars = ['id_user', 'id_item']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db_now = db((db.t_pembelian_bahan.id == request.vars.id_item) & (db.t_pembelian_bahan.id_supplier == id_supplier))
        
        if not db_now.select().first():
            return dict(error="Item not found")
        
        db_now.update(deleted=True)
        return dict(res='ok', id_deleted=request.vars.id_item)
        
    return locals()

@request.restful()
@cors_allow
def kirim_bahan():
    response.view = 'generic.json'
    def PUT(*args, **vars):
        required_vars = ['id_user', 'id_item']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")
        
        id_supplier = get_supplier_id(request.vars.id_user)
        db_now = db((db.t_pembelian_bahan.id == request.vars.id_item) & 
                    (db.t_pembelian_bahan.id_supplier == id_supplier))
        
        if not db_now.select().first():
            return dict(error="Item not found")
        
        db_now.update(status="Dikirim", time_stamp=request.now)
        return dict(res='ok', id_update=request.vars.id_item)
    
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

#------------------------------------------------------------------------------------
## untuk debug
#------------------------------------------------------------------------------------

@request.restful()
@cors_allow
def debug_akun():
    response.view = 'generic.json'
    def GET(*args, **vars):
        # Fetch all user data from the database
        users = db(db.auth_user).select().as_list()
        return dict(users=users)
    return locals()

@request.restful()
@cors_allow
def debug_pengajuan():
    import datetime

    response.view = 'generic.json'
    today = datetime.date.today()

    def GET(*args, **vars):
        rows = db((db.t_kontrak_disdik.tanggal_mulai <= today) & 
                  (db.t_kontrak_disdik.tanggal_selesai >= today) &
                  (db.t_kontrak_disdik.deleted == False)).select().as_list()

        return dict(res=rows)
    return locals()

@request.restful()
@cors_allow
def debug_status_paket():
    response.view = 'generic.json'

    def POST(*args, **vars):
        required_vars = ['id_sekolah', 'id_paket', 'id_vendor', 'status']
        missing_vars = [var for var in required_vars if not request.vars.get(var)]
        if missing_vars:
            raise HTTP(400, f"Missing {', '.join(missing_vars)}")

        db.t_status_paket.insert(
            id_sekolah=request.vars.id_sekolah,
            id_paket=request.vars.id_paket,
            id_vendor=request.vars.id_vendor,
            status=request.vars.status
        )
        return dict(res='ok')

    return locals()

@request.restful()
@cors_allow
def reset_db_status_paket():
    response.view = 'generic.json'

    def GET(*args, **vars):
        db.t_status_paket.truncate()

        return dict(res='ok')
    return locals()

@request.restful()
@cors_allow
def reset_db_pengajuan_paket():
    response.view = 'generic.json'

    def GET(*args, **vars):
        db.t_pengajuan_paket.truncate()

        return dict(res='ok')
    return locals()