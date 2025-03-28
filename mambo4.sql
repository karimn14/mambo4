BEGIN;
USE mambo4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `scheduler_task_deps`;
DROP TABLE IF EXISTS `scheduler_run`;
DROP TABLE IF EXISTS `scheduler_worker`;
DROP TABLE IF EXISTS `scheduler_task`;
DROP TABLE IF EXISTS `map_sekolah_kepala`;
DROP TABLE IF EXISTS `map_disdik_sekolah`;
DROP TABLE IF EXISTS `map_admin_disdik`;
DROP TABLE IF EXISTS `map_supplier_user`;
DROP TABLE IF EXISTS `map_vendor_sekolah`;
DROP TABLE IF EXISTS `map_vendor_user`;
DROP TABLE IF EXISTS `t_periksa_siswa`;
DROP TABLE IF EXISTS `t_pengajuan_paket`;
DROP TABLE IF EXISTS `t_pembelian_bahan`;
DROP TABLE IF EXISTS `t_menu_supplier`;
DROP TABLE IF EXISTS `t_kontrak_disdik`;
DROP TABLE IF EXISTS `t_keluhan_user`;
DROP TABLE IF EXISTS `t_siswa`;
DROP TABLE IF EXISTS `t_status_paket`;
DROP TABLE IF EXISTS `t_harga_supplier`;
DROP TABLE IF EXISTS `m_satuan_menu`;
DROP TABLE IF EXISTS `m_propinsi`;
DROP TABLE IF EXISTS `m_paket`;
DROP TABLE IF EXISTS `m_vendor`;
DROP TABLE IF EXISTS `m_supplier`;
DROP TABLE IF EXISTS `m_sekolah`;
DROP TABLE IF EXISTS `m_disdik`;
DROP TABLE IF EXISTS `m_kelurahan_desa`;
DROP TABLE IF EXISTS `m_kodepos`;
DROP TABLE IF EXISTS `m_satuan_supplier`;
DROP TABLE IF EXISTS `auth_membership`;
DROP TABLE IF EXISTS `auth_group`;
DROP TABLE IF EXISTS `auth_event`;
DROP TABLE IF EXISTS `auth_cas`;
DROP TABLE IF EXISTS `auth_permission`;
DROP TABLE IF EXISTS `auth_user`;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(128),
    `last_name` VARCHAR(128),
    `email` VARCHAR(512),
    `password` VARCHAR(512),
    `registration_key` VARCHAR(512),
    `reset_password_key` VARCHAR(512),
    `registration_id` VARCHAR(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `role` VARCHAR(512),
    `description` TEXT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. auth_membership
CREATE TABLE IF NOT EXISTS `auth_membership` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT,
    `group_id` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`group_id`) REFERENCES `auth_group`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `group_id` INT,
    `name` VARCHAR(512),
    `table_name` VARCHAR(512),
    `record_id` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`group_id`) REFERENCES `auth_group`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. auth_cas
CREATE TABLE IF NOT EXISTS `auth_cas` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT,
    `created_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `service` VARCHAR(512),
    `ticket` VARCHAR(512),
    `renew` VARCHAR(1),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. auth_event
CREATE TABLE IF NOT EXISTS `auth_event` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `time_stamp` TIMESTAMP,
    `client_ip` VARCHAR(512),
    `user_id` INT,
    `origin` VARCHAR(512),
    `description` TEXT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. m_kelurahan_desa
CREATE TABLE IF NOT EXISTS `m_kelurahan_desa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_kecamatan` VARCHAR(512),
    `kelurahan_desa` VARCHAR(512),
    `kode_pos` INT,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. m_kodepos
CREATE TABLE IF NOT EXISTS `m_kodepos` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_kelurahan_desa` VARCHAR(512),
    `id_kecamatan` VARCHAR(512),
    `id_kabupaten_kota` VARCHAR(512),
    `id_propinsi` VARCHAR(512),
    `kode_pos` VARCHAR(512),
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. m_disdik
CREATE TABLE IF NOT EXISTS `m_disdik` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_disdik` VARCHAR(512),
    `alamat` VARCHAR(512),
    `id_kelurahan_desa` INT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `id_kode_pos` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_kelurahan_desa`) REFERENCES `m_kelurahan_desa`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_kode_pos`) REFERENCES `m_kodepos`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. m_paket
CREATE TABLE IF NOT EXISTS `m_paket` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_paket` VARCHAR(512),
    `pagu_harga` INT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `kalori` DOUBLE,
    `id_vendor` INT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. m_propinsi
CREATE TABLE IF NOT EXISTS `m_propinsi` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `propinsi` VARCHAR(512),
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. m_satuan_menu
CREATE TABLE IF NOT EXISTS `m_satuan_menu` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_satuan` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. m_satuan_supplier
CREATE TABLE IF NOT EXISTS `m_satuan_supplier` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_satuan` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 14. m_sekolah
CREATE TABLE IF NOT EXISTS `m_sekolah` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_sekolah` VARCHAR(512),
    `alamat` VARCHAR(512),
    `id_kelurahan_desa` INT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `id_kode_pos` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_kelurahan_desa`) REFERENCES `m_kelurahan_desa`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_kode_pos`) REFERENCES `m_kodepos`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 15. m_supplier
CREATE TABLE IF NOT EXISTS `m_supplier` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_supplier` VARCHAR(512),
    `alamat` VARCHAR(512),
    `id_kelurahan_desa` INT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `id_kode_pos` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_kelurahan_desa`) REFERENCES `m_kelurahan_desa`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_kode_pos`) REFERENCES `m_kodepos`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 16. m_vendor
CREATE TABLE IF NOT EXISTS `m_vendor` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `nama_vendor` VARCHAR(512),
    `alamat` VARCHAR(512),
    `id_kelurahan_desa` INT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `id_kode_pos` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_kelurahan_desa`) REFERENCES `m_kelurahan_desa`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_kode_pos`) REFERENCES `m_kodepos`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 17. map_admin_disdik
CREATE TABLE IF NOT EXISTS `map_admin_disdik` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_disdik` VARCHAR(512),
    `id_admin` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 18. map_disdik_sekolah
CREATE TABLE IF NOT EXISTS `map_disdik_sekolah` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_sekolah` VARCHAR(512),
    `id_disdik` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 19. map_sekolah_kepala
CREATE TABLE IF NOT EXISTS `map_sekolah_kepala` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_sekolah` VARCHAR(512),
    `id_kepala_sekolah` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 20. map_supplier_user
CREATE TABLE IF NOT EXISTS `map_supplier_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_supplier` VARCHAR(512),
    `id_user` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 21. map_vendor_sekolah
CREATE TABLE IF NOT EXISTS `map_vendor_sekolah` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_vendor` VARCHAR(512),
    `id_sekolah` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 22. map_vendor_user
CREATE TABLE IF NOT EXISTS `map_vendor_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_vendor` VARCHAR(512),
    `id_user` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 23. scheduler_task
CREATE TABLE IF NOT EXISTS `scheduler_task` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `application_name` VARCHAR(512),
    `task_name` VARCHAR(512),
    `group_name` VARCHAR(512),
    `status` VARCHAR(512),
    `broadcast` VARCHAR(1),
    `function_name` VARCHAR(512),
    `uuid` VARCHAR(255) UNIQUE,
    `args` TEXT,
    `vars` TEXT,
    `enabled` VARCHAR(1),
    `start_time` TIMESTAMP,
    `next_run_time` TIMESTAMP,
    `stop_time` TIMESTAMP,
    `repeats` INT,
    `retry_failed` INT,
    `period` INT,
    `prevent_drift` VARCHAR(1),
    `cronline` VARCHAR(512),
    `timeout` INT,
    `sync_output` INT,
    `times_run` INT,
    `times_failed` INT,
    `last_run_time` TIMESTAMP,
    `assigned_worker_name` VARCHAR(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 24. scheduler_task_deps
CREATE TABLE IF NOT EXISTS `scheduler_task_deps` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `job_name` VARCHAR(512),
    `task_parent` INT,
    `task_child` INT,
    `can_visit` VARCHAR(1),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`task_child`) REFERENCES `scheduler_task`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 25. scheduler_run
CREATE TABLE IF NOT EXISTS `scheduler_run` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `task_id` INT,
    `status` VARCHAR(512),
    `start_time` TIMESTAMP,
    `stop_time` TIMESTAMP,
    `run_output` TEXT,
    `run_result` TEXT,
    `traceback` TEXT,
    `worker_name` VARCHAR(512),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`task_id`) REFERENCES `scheduler_task`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 26. scheduler_worker
CREATE TABLE IF NOT EXISTS `scheduler_worker` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `worker_name` VARCHAR(255) UNIQUE,
    `first_heartbeat` TIMESTAMP,
    `last_heartbeat` TIMESTAMP,
    `status` VARCHAR(512),
    `is_ticker` VARCHAR(1),
    `group_names` TEXT,
    `worker_stats` TEXT,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 27. t_harga_supplier
CREATE TABLE IF NOT EXISTS `t_harga_supplier` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_supplier` VARCHAR(512),
    `nama_item` VARCHAR(512),
    `volume` INT,
    `harga` INT,
    `id_satuan_supplier` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 28. t_keluhan_user
CREATE TABLE IF NOT EXISTS `t_keluhan_user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_user` VARCHAR(512),
    `keluhan` TEXT,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 29. t_kontrak_disdik
CREATE TABLE IF NOT EXISTS `t_kontrak_disdik` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_disdik` INT,
    `id_vendor` INT,
    `nama` VARCHAR(512),
    `nip_npwp` VARCHAR(512),
    `jabatan` VARCHAR(512),
    `alamat` VARCHAR(512),
    `instansi` VARCHAR(512),
    `jenis_paket` VARCHAR(512),
    `jumlah_kalori` DOUBLE,
    `jumlah_paket_per_hari` INT,
    `tanggal_mulai` DATE,
    `tanggal_selesai` DATE,
    `durasi` INT,
    `total_biaya_kontrak` INT,
    `deleted` VARCHAR(1),
    `bukti_kontrak` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `id_sekolah` INT,
    `id_paket` INT,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_disdik`) REFERENCES `m_disdik`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_paket`) REFERENCES `m_paket`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_sekolah`) REFERENCES `m_sekolah`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_vendor`) REFERENCES `m_vendor`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 30. t_menu_supplier
CREATE TABLE IF NOT EXISTS `t_menu_supplier` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_supplier` VARCHAR(512),
    `nama_item` VARCHAR(512),
    `volume` INT,
    `harga` INT,
    `id_satuan_supplier` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 31. t_pembelian_bahan
CREATE TABLE IF NOT EXISTS `t_pembelian_bahan` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_supplier` VARCHAR(512),
    `id_vendor` VARCHAR(512),
    `nama_vendor` VARCHAR(512),
    `nama_item` VARCHAR(512),
    `volume` INT,
    `harga` INT,
    `id_satuan_supplier` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `status` VARCHAR(512),
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 32. t_pengajuan_paket
CREATE TABLE IF NOT EXISTS `t_pengajuan_paket` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_vendor` VARCHAR(512),
    `id_disdik` VARCHAR(512),
    `id_sekolah` VARCHAR(512),
    `id_paket` VARCHAR(512),
    `jumlah` INT,
    `jenis_paket` VARCHAR(512),
    `approve` VARCHAR(1),
    `time_stamp_setuju` TIMESTAMP,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `time_stamp_update` TIMESTAMP,
    `time_stamp_dibuat` TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 33. t_periksa_siswa
CREATE TABLE IF NOT EXISTS `t_periksa_siswa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_siswa` VARCHAR(512),
    `tinggi_badan` DOUBLE,
    `berat_badan` DOUBLE,
    `tanggal_pengukuran` DATE,
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 34. t_siswa
CREATE TABLE IF NOT EXISTS `t_siswa` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_sekolah` VARCHAR(512),
    `nama` VARCHAR(512),
    `tanggal_lahir` DATE,
    `jenis_kelamin` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `tempat_lahir` VARCHAR(512),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 35. t_status_paket
CREATE TABLE IF NOT EXISTS `t_status_paket` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `id_t_pengajuan_paket` VARCHAR(512),
    `id_disdik` INT,
    `id_sekolah` INT,
    `id_paket` INT,
    `id_vendor` INT,
    `status` VARCHAR(512),
    `time_stamp` TIMESTAMP,
    `deleted` VARCHAR(1),
    `ts_diproses_ditolak` TIMESTAMP,
    `ts_dikirim` TIMESTAMP,
    `ts_diterima` TIMESTAMP,
    `ts_last_update` TIMESTAMP,
    `ts_dibuat` TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`id_disdik`) REFERENCES `m_disdik`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_paket`) REFERENCES `m_paket`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_sekolah`) REFERENCES `m_sekolah`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`id_vendor`) REFERENCES `m_vendor`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



SET FOREIGN_KEY_CHECKS = 1;
COMMIT;
