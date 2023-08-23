from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(200), unique=True)
    password = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    nomorhp = db.Column(db.VARCHAR(200))
    lvl = db.Column(db.VARCHAR(200))


class Kuisioner_Individu(db.Model):
# class Deskripsi_Individu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Analisis_Pengeluaran_Perkapita = db.Column(db.Integer)
    Nomor_KK = db.Column(db.Integer)
    Jumlah_Anggota_Keluarga = db.Column(db.Integer)
    Nama_Kepala_Keluarga = db.Column(db.VARCHAR(200))
    Jenis_Kelamin_Keluarga = db.Column(db.VARCHAR(200))
    NIK = db.Column(db.Integer)
    Nama_Lengkap = db.Column(db.VARCHAR(200))
    Jenis_Kelamin = db.Column(db.VARCHAR(200))
    Tempat_Lahir = db.Column(db.VARCHAR(200))
    Tanggal_Lahir = db.Column(db.VARCHAR(200))
    # tambahan alamat
    Alamat_Tempat_Tinggal = db.Column(db.VARCHAR(200))
    Provinsi = db.Column(db.VARCHAR(200))
    Kota_Kabupaten = db.Column(db.VARCHAR(200))
    Kecamatan = db.Column(db.VARCHAR(200))
    Kelurahan_Atau_Desa= db.Column(db.VARCHAR(200))
    Status_Perkawinan = db.Column(db.VARCHAR(200))
    Agama = db.Column(db.VARCHAR(200))
    Suku = db.Column(db.VARCHAR(200))
    Warga_Negara = db.Column(db.VARCHAR(200))
    Nomor_Telp = db.Column(db.VARCHAR(200))
    Nomor_Wa = db.Column(db.VARCHAR(200))
    Email = db.Column(db.VARCHAR(200))
    Media_Sosial = db.Column(db.VARCHAR(200))

# class Deskripsi_Pekerjaan(db.Model):    
    Kondisi_Pekerjaan = db.Column(db.VARCHAR(200))
    Pekerjaan_Utama = db.Column(db.VARCHAR(200))
    Jaminan_Sosial_Ketenagakerjaan = db.Column(db.VARCHAR(200))
    Penghasilan_Sebulan_Terakhir = db.Column(db.VARCHAR(200))
    Pengeluaran_Sebulan_Terakhir = db.Column(db.VARCHAR(200))
    Kepemilikan_Rumah = db.Column(db.VARCHAR(200))
    Kepemilikan_Lahan_Luas = db.Column(db.Integer)
    
# class Deskripsi_Kesehatan(db.Model):    
    Penyakit_Setahun_Terakhir = db.Column(db.VARCHAR(200))
    Fasilitas_Kesehatan_Dikunjungi = db.Column(db.VARCHAR(200))
    Jumlah_Berapa_Kali_Fasilitas_Kesehatan_Dikunjungi = db.Column(db.Integer)
    Jaminan_Kesehatan_Asuransi_KIS = db.Column(db.VARCHAR(200))
    Disabilitas = db.Column(db.VARCHAR(200))

# class Deskripsi_Pendidikan(db.Model):   
    Pendidikan_Terakhir = db.Column(db.VARCHAR(200))
    Bahasa_Digunakan_Dirumah = db.Column(db.VARCHAR(200))
    Bahasa_Digunakan_Disekolah_Kantor_Tempat_Kerja = db.Column(db.VARCHAR(200))
    Kerja_Bakti_Setahun_Terakhir = db.Column(db.Integer)
    Siskamling_Setahun_Terakhir = db.Column(db.Integer)
    Pesta_Rakyat_atau_Adat_Terakhir_Dilaksanakan = db.Column(db.Integer)
    Menolong_warga_Mengalami_Kematian_Setahun_Terakhir = db.Column(db.Integer)
    Menolong_warga_Mengalami_Sakit_Setahun_Terakhir = db.Column(db.Integer)
    Menolong_warga_Mengalami_Kecelakaan_Setahun_Terakhir = db.Column(db.Integer)
  
   
class data_peta(UserMixin, db.Model):
    id_datapeta = db.Column(db.Integer, primary_key=True)
    Nama_File_SHP = db.Column(db.VARCHAR(200))
    Provinsi = db.Column(db.VARCHAR(200))
    KotaKabupaten = db.Column(db.VARCHAR(200))
    Kecamatan = db.Column(db.VARCHAR(200))
    Desa = db.Column(db.VARCHAR(200))
    Type_SHP = db.Column(db.JSON)



