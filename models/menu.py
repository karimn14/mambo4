# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    if auth.has_membership('super_admin'):

        response.menu += [
            (T('Master Data'), False, '#', [
                (T('Daftar Disdik'), False, URL('master_data', 'master_disdik')),
                (T('Daftar Sekolah'), False, URL('master_data', 'master_sekolah')),
                (T('Daftar Supplier'), False, URL('master_data', 'master_supplier')),
                (T('Daftar Vendor'), False, URL('master_data', 'master_vendor')),
                (T('Daftar Paket'), False, URL('master_data', 'master_paket')),
                (T('Daftar Satuan Menu'), False, URL('master_data', 'master_satuan_menu')),
                (T('Daftar Satuan Supplier'), False, URL('master_data', 'master_satuan_supplier ')),
            ]),
            (T('Vendor'), False, '#', [
                (T('List Mapping Vendor-ID'), False, URL('vendor', 'list_map_vendor_user_id')),
                (T('Mapping Vendor-ID'), False, URL('vendor', 'map_vendor_user_id')),
                (T('List Mapping Vendor-Sekolah'), False, URL('vendor', 'list_map_vendor_sekolah')),
            ]),
            (T('Supplier'), False, '#', [
                (T('List Mapping Supplier-ID'), False, URL('supplier', 'list_map_supplier_user')),
                (T('Mapping Supplier-ID'), False, URL('supplier', 'map_supplier_user_id')),
            ]),            
            (T('Sekolah'), False, '#', [
                (T('List Mapping Disdik-Sekolah'), False, URL('sekolah', 'list_map_sekolah_disdik')),
                (T('Mapping Disdik-Sekolah'), False, URL('sekolah', 'map_sekolah_disdik')),
                (T('List Mapping Sekolah-Kepala Sekolah'), False, URL('sekolah', 'list_map_sekolah_kepala')),
                (T('Mapping Sekolah-Kepala Sekolah'), False, URL('sekolah', 'map_sekolah_kepala')),
            ]),
            (T('Dinas Pendidikan'), False, '#', [
                (T('List Mapping Admin Disdik-ID'), False, URL('disdik', 'list_map_admin_disdik_user_id')),
                (T('Mapping Admin Disdik-ID'), False, URL('disdik', 'map_admin_disdik_user_id')),
            ]),
        ]

    if auth.has_membership('supplier'):
            response.menu += [
            (T('Supplier'), False, '#', [
                (T('Item Supplier'), False, URL('supplier', 'item_supplier')),
            ]),
        ]

    if auth.has_membership('vendor'):
        response.menu += [
            (T('Vendor'), False, '#', [
                (T('Pesanan'), False, URL('vendor', 'pesanan')), #katering

            ]),
        ]
   
    if auth.has_membership('kepala_sekolah'):
        response.menu += [
            (T('Sekolah'), False, '#', [
                #(T('Pengajuan Paket Makan'), False, URL('sekolah', 'pengajuan_paket_makan')),
                (T('Tanda Terima Paket'), False, URL('sekolah', 'tanda_terima_paket')),
                (T('Data Perkembangan Siswa'), False, URL('sekolah', 'status_siswa')),
                
            ]),
        ]

    if auth.has_membership('disdik_admin'):
        response.menu += [
            (T('Dinas Pendidikan'), False, '#', [
                #(T('Persetujuan Paket'), False, URL('disdik', 'persetujuan_paket')),
                (T('Pemberian Paket'), False, URL('disdik', 'pemberian_paket')),
                (T('Daftar Pemberian Paket'), False, URL('disdik', 'daftar_pemberian_paket')),
                (T('Daftar Penerimaan Paket'), False, URL('disdik', 'daftar_penerimaan_paket')),                
            ]),
        ]
    

