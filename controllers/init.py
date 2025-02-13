def init_all():
	init_user()
	init_role_and_membership()
	return dict(a='b')

def init_entity():
	init_sekolah()
	init_disdik()
	init_vendor()
	init_supplier()
	init_map_sekolah_disdik()

	init_map_user_sekolah()
	init_map_user_disdik()
	init_map_user_vendor()
	init_map_user_supplier()
	init_satuan_supplier()
	init_item_supplier()

	init_paket_makan()
	return dict(a='b')

def init_sekolah():
	db.m_sekolah.update_or_insert(db.m_sekolah.id==1, nama_sekolah='SDN 1', alamat='Raya Laswi', id_kelurahan_desa=25363, id_kode_pos=25373)
	db.m_sekolah.update_or_insert(db.m_sekolah.id==2, nama_sekolah='SDN 2', alamat='Raya Laswi', id_kelurahan_desa=25363, id_kode_pos=25373)
	db.m_sekolah.update_or_insert(db.m_sekolah.id==3, nama_sekolah='SMPN 12', alamat='Jembatan Opat', id_kelurahan_desa=27889, id_kode_pos= 27899)
	db.m_sekolah.update_or_insert(db.m_sekolah.id==4, nama_sekolah='SMPN 13', alamat='Pelajar Pejuang 45', id_kelurahan_desa=28335, id_kode_pos= 28345)
	return dict(a='b')

def init_disdik():
	db.m_disdik.update_or_insert(db.m_disdik.id==1, nama_disdik='Disdik Bandung', alamat='Jl Pandu', id_kelurahan_desa=29099, id_kode_pos= 29109)
	return dict(a='b')

def init_vendor():
	db.m_vendor.update_or_insert(db.m_vendor.id==1, nama_vendor='Katering 1', alamat='Buah batu', id_kelurahan_desa=25745, id_kode_pos= 25755)
	db.m_vendor.update_or_insert(db.m_vendor.id==2, nama_vendor='Katering 2', alamat='Jl Sukabumi', id_kelurahan_desa=27540, id_kode_pos= 27550)
	db.m_vendor.update_or_insert(db.m_vendor.id==3, nama_vendor='Katering 3', alamat='Babakan Jati 1', id_kelurahan_desa=25550, id_kode_pos= 25560)
	db.m_vendor.update_or_insert(db.m_vendor.id==4, nama_vendor='Katering 4', alamat='Jl Pagar Betis', id_kelurahan_desa=26622, id_kode_pos= 26632)#sumedang
	return dict(a='b')

def init_supplier():
	db.m_supplier.update_or_insert(db.m_supplier.id==1, nama_supplier='Supplier 1', alamat='Ibrahim Adjie', id_kelurahan_desa=25550, id_kode_pos= 25560)
	db.m_supplier.update_or_insert(db.m_supplier.id==2, nama_supplier='Supplier 2', alamat='Jl Korawa', id_kelurahan_desa=29099, id_kode_pos= 29109)
	db.m_supplier.update_or_insert(db.m_supplier.id==3, nama_supplier='Supplier 3', alamat='Jl Siliwangi', id_kelurahan_desa=25363, id_kode_pos= 25373)
	db.m_supplier.update_or_insert(db.m_supplier.id==4, nama_supplier='Supplier 4', alamat='Ciraja Girang', id_kelurahan_desa=28567, id_kode_pos= 28577)
	return dict(a='b')

def init_map_sekolah_disdik():
	db.map_disdik_sekolah.update_or_insert(db.map_disdik_sekolah.id==1, id_sekolah=1, id_disdik=1)
	db.map_disdik_sekolah.update_or_insert(db.map_disdik_sekolah.id==2, id_sekolah=2, id_disdik=1)
	db.map_disdik_sekolah.update_or_insert(db.map_disdik_sekolah.id==3, id_sekolah=3, id_disdik=1)
	db.map_disdik_sekolah.update_or_insert(db.map_disdik_sekolah.id==4, id_sekolah=4, id_disdik=1)
	return dict(a='b')

def init_map_user_sekolah():
	db.map_sekolah_kepala.update_or_insert(db.map_sekolah_kepala.id==1, id_sekolah=1, id_kepala_sekolah=2)
	return dict(a='b')

def init_map_user_disdik():
	db.map_admin_disdik.update_or_insert(db.map_admin_disdik.id==1, id_disdik=1, id_admin=3)
	return dict(a='b')

def init_map_user_vendor():
	db.map_vendor_user.update_or_insert(db.map_vendor_user.id==1, id_vendor=1, id_user=5)
	db.map_vendor_user.update_or_insert(db.map_vendor_user.id==2, id_vendor=2, id_user=6)
	return dict(a='b')

def init_map_user_supplier():
	db.map_supplier_user.update_or_insert(db.map_supplier_user.id==1, id_supplier=1, id_user=4)
	db.map_supplier_user.update_or_insert(db.map_supplier_user.id==2, id_supplier=2, id_user=7)
	return dict(a='b')

def init_satuan_supplier():
	db.m_satuan_supplier.update_or_insert(db.m_satuan_supplier.id==1, nama_satuan='kg')
	db.m_satuan_supplier.update_or_insert(db.m_satuan_supplier.id==2, nama_satuan='liter')
	db.m_satuan_supplier.update_or_insert(db.m_satuan_supplier.id==3, nama_satuan='karton')
	db.m_satuan_supplier.update_or_insert(db.m_satuan_supplier.id==4, nama_satuan='ikat')
	return dict(a='b')

def init_item_supplier():
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==1, id_supplier = 1,nama_item = 'Beras',volume = 5,harga = 50000,id_satuan_supplier =  1)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==2, id_supplier = 1,nama_item = 'Minyak',volume = 5,harga = 40000,id_satuan_supplier =  2)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==3, id_supplier = 1,nama_item = 'Telur',volume = 15,harga = 25000,id_satuan_supplier =  1)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==4, id_supplier = 1,nama_item = 'Mentega',volume = 12,harga = 150000,id_satuan_supplier =  3)

	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==1, id_supplier = 2,nama_item = 'Seledri',volume = 5,harga = 5000,id_satuan_supplier =  4)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==2, id_supplier = 2,nama_item = 'Bawang merah',volume = 5,harga = 45000,id_satuan_supplier =  1)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==3, id_supplier = 2,nama_item = 'Daging Ayam',volume = 1,harga = 55000,id_satuan_supplier =  1)
	db.t_harga_supplier.update_or_insert(db.t_harga_supplier.id==4, id_supplier = 2,nama_item = 'Daging sapi',volume = 1,harga = 150000,id_satuan_supplier =  1)
	return dict(a='b')

def init_map_vendor_sekolah():
	db.map_vendor_sekolah.update_or_insert(db.map_vendor_sekolah.id==1, id_vendor=1, id_sekolah=1)
	db.map_vendor_sekolah.update_or_insert(db.map_vendor_sekolah.id==2, id_vendor=1, id_sekolah=2)
	db.map_vendor_sekolah.update_or_insert(db.map_vendor_sekolah.id==3, id_vendor=1, id_sekolah=3)
	db.map_vendor_sekolah.update_or_insert(db.map_vendor_sekolah.id==4, id_vendor=2, id_sekolah=4)
	return dict(a='b')

def init_paket_makan():
	db.m_paket.update_or_insert(db.m_paket.id==1, nama_paket="Makan Siang 1", pagu_harga=10000, kalori=666.5)
	db.m_paket.update_or_insert(db.m_paket.id==2, nama_paket="Makan Siang 2", pagu_harga=15000, kalori=766.5)
	db.m_paket.update_or_insert(db.m_paket.id==3, nama_paket="Makan Siang 3", pagu_harga=20000, kalori=800)
	return dict(a='b')

def init_user():
	db.auth_user.update_or_insert(db.auth_user.id==1, first_name='Super', last_name='Admin', email='super_admin@local.test')
	db(db.auth_user.id==1).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==2, first_name='Kepala', last_name='Sekolah', email='kepala_sekolah@local.test')
	db(db.auth_user.id==2).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==3, first_name='Disdik', last_name='Regional', email='disdik@local.test')
	db(db.auth_user.id==3).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==4, first_name='Supplier', last_name='1', email='supplier1@local.test')
	db(db.auth_user.id==4).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==5, first_name='Vendor', last_name='1', email='vendor1@local.test')
	db(db.auth_user.id==5).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==6, first_name='Vendor', last_name='2', email='vendor2@local.test')
	db(db.auth_user.id==6).validate_and_update(password='1234')

	db.auth_user.update_or_insert(db.auth_user.id==7, first_name='Supplier', last_name='2', email='supplier2@local.test')
	db(db.auth_user.id==7).validate_and_update(password='1234')

	return dict(a='b')

def init_role_and_membership():
	db.auth_group.update_or_insert(db.auth_group.id==1, role = 'super_admin', description = 'Super Admin untuk Mambo')
	db.auth_group.update_or_insert(db.auth_group.id==2, role = 'kepala_sekolah', description = 'Kepala Sekolah')
	db.auth_group.update_or_insert(db.auth_group.id==3, role = 'disdik_admin', description = 'Admin dari Disdik Regional')
	db.auth_group.update_or_insert(db.auth_group.id==4, role = 'supplier', description = 'Supplier')
	db.auth_group.update_or_insert(db.auth_group.id==5, role = 'vendor', description = 'Vendor/Katering')
	auth.add_membership(1, 1)
	auth.add_membership(2, 2)	
	auth.add_membership(3, 3)	
	auth.add_membership(4, 4)
	auth.add_membership(5, 5)
	auth.add_membership(5, 6)
	auth.add_membership(4, 7)
	return dict(a='b')

def init_propinsi():
	return dict(a='b')
	