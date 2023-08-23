import os
from msilib import add_data
import numpy as np
import folium
import patoolib
import folium
import json
import geopandas as gpd
from folium.plugins import MousePosition
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Kuisioner_Individu, User, data_peta
from . import db

main = Blueprint('homepage', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("homepage.html", name=current_user.nama)
    return render_template("homepage.html")



@main.route("/dashboard")
@login_required
def index():
    Kuisindiv = Kuisioner_Individu.query.all()

    data = '600000'
    minus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita <= data).count())
    plus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita > data).count())
    totaldatkus = Kuisioner_Individu.query.count()

    # PerKem = Persentase Kemiskinan 
    # analisis persentase pengeluaran perkapita diatas kemiskinan      
    perkemplus = plus / Kuisioner_Individu.query.count()*100
    
    # analisis persentase pengeluaran perkapita dibawah kemiskinan
    perkemminus = minus / Kuisioner_Individu.query.count()*100

    user = User.query.all()


    return render_template('index.html', Kuisioner_Individu=Kuisindiv, totaldatkus=totaldatkus, perkemplus=perkemplus, perkemminus=perkemminus, Minus=minus, Plus=plus, user=user)


@main.route("/base")
@login_required
def base():
    user = User.query.all()
    return render_template('base.html', user=user)

@main.route("/forms", methods=['GET', 'POST'])
@main.route("/forms/<id>", methods=['GET','POST'])
@login_required
def forms(id=None):
    if id:
        update = Kuisioner_Individu.query.filter_by(id=id).first()
        Provinsi = data_peta.query.all()
        
        return render_template('forms.html', row = update, id=id,Provinsi=Provinsi)
    else:
        if request.method == 'POST' :
            edit = request.form.get('edit')
            print (edit)
            if edit:
                update = Kuisioner_Individu.query.get(request.form.get('edit'))

                # Analisis Pengeluaran Perkapita
                ldata = int(update.Pengeluaran_Sebulan_Terakhir) / int(update.Jumlah_Anggota_Keluarga) 
                update.Analisis_Pengeluaran_Perkapita=ldata

                update.Nomor_KK=request.form['NoKK']
                update.Jumlah_Anggota_Keluarga=request.form['JumlahAK']
                update.Nama_Kepala_Keluarga=request.form['NamaKK']
                update.Jenis_Kelamin_Keluarga=request.form['JKKK']
                update.NIK=request.form['NIK']
                update.Nama_Lengkap=request.form['Namalkp']
                update.Jenis_Kelamin=request.form['JK']
                update.Tempat_Lahir=request.form['tempatlhr']
                update.Tanggal_Lahir=request.form['tgllhr']
                # tambahan alamat
                update.Alamat_Tempat_Tinggal=request.form['alamatttg']
                update.Provinsi=request.form['provinsi']
                update.Kota_Kabupaten=request.form['kotkab']
                update.Kecamatan=request.form['kec']
                update.Kelurahan_Atau_Desa=request.form['keldes']

                

                update.Status_Perkawinan=request.form['Skwn']
                update.Agama=request.form['Agama']
                update.Suku=request.form['Suku']
                update.Warga_Negara=request.form['warganeg']
                update.Nomor_Telp=request.form['notelp']
                update.Nomor_Wa=request.form['nowa']
                update.Email=request.form['email']
                update.Media_Sosial=request.form['akunmedsos']
                
                # elif request.form ['submit'] =='deskjob': 
                update.Kondisi_Pekerjaan=request.form['konjob']
                update.Pekerjaan_Utama=request.form['jobut']
                update.Jaminan_Sosial_Ketenagakerjaan=request.form['bpjs']
                update.Penghasilan_Sebulan_Terakhir=request.form['peng1bln']
                update.Pengeluaran_Sebulan_Terakhir=request.form['penlu1bln']
                update.Kepemilikan_Rumah=request.form['keprmh']
                update.Kepemilikan_Lahan_Luas=request.form['keplhn']

                # elif request.form ['submit'] =='deskkes':
                update.Penyakit_Setahun_Terakhir=request.form['penyakit']
                update.Fasilitas_Kesehatan_Dikunjungi=request.form['faskes']
                update.Jumlah_Berapa_Kali_Fasilitas_Kesehatan_Dikunjungi=request.form['jmlhfaskes']
                update.Jaminan_Kesehatan_Asuransi_KIS=request.form['kis']
                update.Disabilitas=request.form['disabil']

                # elif request.form ['submit'] =='deskpend':
                update.Pendidikan_Terakhir=request.form['pendidk']
                update.Bahasa_Digunakan_Dirumah=request.form['bhs']
                update.Bahasa_Digunakan_Disekolah_Kantor_Tempat_Kerja=request.form['bhsskl']
                update.Kerja_Bakti_Setahun_Terakhir=request.form['krjbkti']
                update.Siskamling_Setahun_Terakhir=request.form['siskaeee']
                update.Pesta_Rakyat_atau_Adat_Terakhir_Dilaksanakan=request.form['pestaryt']
                update.Menolong_warga_Mengalami_Kematian_Setahun_Terakhir=request.form['tlngdet']
                update.Menolong_warga_Mengalami_Sakit_Setahun_Terakhir=request.form['tlngskt']
                update.Menolong_warga_Mengalami_Kecelakaan_Setahun_Terakhir=request.form['tlnglaka']

                db.session.commit()
                flash("Data berhasil diubah")

                return redirect(url_for('homepage.tables'))
                
            # if request.form ['submit'] =='deskindiv':
            Nomor_KK=request.form['NoKK']
            Jumlah_Anggota_Keluarga=request.form['JumlahAK']
            Nama_Kepala_Keluarga=request.form['NamaKK']
            Jenis_Kelamin_Keluarga=request.form['JKKK']
            NIK=request.form['NIK']
            Nama_Lengkap=request.form['Namalkp']
            Jenis_Kelamin=request.form['JK']
            Tempat_Lahir=request.form['tempatlhr']
            Tanggal_Lahir=request.form['tgllhr']
            # tambahan alamat
            Alamat_Tempat_Tinggal=request.form['alamatttg']
            Provinsi=request.form['provinsi']
            Kota_Kabupaten=request.form['kotkab']
            Kecamatan=request.form['kec']
            Kelurahan_Atau_Desa=request.form['keldes']
            
            Status_Perkawinan=request.form['Skwn']
            Agama=request.form['Agama']
            Suku=request.form['Suku']
            Warga_Negara=request.form['warganeg']
            Nomor_Telp=request.form['notelp']
            Nomor_Wa=request.form['nowa']
            Email=request.form['email']
            Media_Sosial=request.form['akunmedsos']
            
            # elif request.form ['submit'] =='deskjob': 
            Kondisi_Pekerjaan=request.form['konjob']
            Pekerjaan_Utama=request.form['jobut']
            Jaminan_Sosial_Ketenagakerjaan=request.form['bpjs']
            Penghasilan_Sebulan_Terakhir=request.form['peng1bln']
            Pengeluaran_Sebulan_Terakhir=request.form['penlu1bln']
            Kepemilikan_Rumah=request.form['keprmh']
            Kepemilikan_Lahan_Luas=request.form['keplhn']

            # elif request.form ['submit'] =='deskkes':
            Penyakit_Setahun_Terakhir=request.form['penyakit']
            Fasilitas_Kesehatan_Dikunjungi=request.form['faskes']
            Jumlah_Berapa_Kali_Fasilitas_Kesehatan_Dikunjungi=request.form['jmlhfaskes']
            Jaminan_Kesehatan_Asuransi_KIS=request.form['kis']
            Disabilitas=request.form['disabil']

            # elif request.form ['submit'] =='deskpend':
            Pendidikan_Terakhir=request.form['pendidk']
            Bahasa_Digunakan_Dirumah=request.form['bhs']
            Bahasa_Digunakan_Disekolah_Kantor_Tempat_Kerja=request.form['bhsskl']
            Kerja_Bakti_Setahun_Terakhir=request.form['krjbkti']
            Siskamling_Setahun_Terakhir=request.form['siskaeee']
            Pesta_Rakyat_atau_Adat_Terakhir_Dilaksanakan=request.form['pestaryt']
            Menolong_warga_Mengalami_Kematian_Setahun_Terakhir=request.form['tlngdet']
            Menolong_warga_Mengalami_Sakit_Setahun_Terakhir=request.form['tlngskt']
            Menolong_warga_Mengalami_Kecelakaan_Setahun_Terakhir=request.form['tlnglaka']

            # Analisis Pengeluaran Perkapita
            ldata = int(Pengeluaran_Sebulan_Terakhir) / int(Jumlah_Anggota_Keluarga) 


            add_data_Kuisioner_Individu = Kuisioner_Individu(Analisis_Pengeluaran_Perkapita=ldata,
                                            Nomor_KK=Nomor_KK,
                                            Jumlah_Anggota_Keluarga=Jumlah_Anggota_Keluarga,
                                            Nama_Kepala_Keluarga=Nama_Kepala_Keluarga,
                                            Jenis_Kelamin_Keluarga=Jenis_Kelamin_Keluarga,
                                            NIK=NIK,
                                            Nama_Lengkap=Nama_Lengkap,
                                            Jenis_Kelamin=Jenis_Kelamin,
                                            Tempat_Lahir=Tempat_Lahir,
                                            Tanggal_Lahir=Tanggal_Lahir,
                                            # tambahan alamat
                                            Alamat_Tempat_Tinggal=Alamat_Tempat_Tinggal,
                                            Provinsi=Provinsi,
                                            Kota_Kabupaten=Kota_Kabupaten,
                                            Kecamatan=Kecamatan,
                                            Kelurahan_Atau_Desa=Kelurahan_Atau_Desa,

                                                                                       

                                            Status_Perkawinan=Status_Perkawinan,
                                            Agama=Agama,
                                            Suku=Suku,
                                            Warga_Negara=Warga_Negara,
                                            Nomor_Telp=Nomor_Telp,
                                            Nomor_Wa=Nomor_Wa,
                                            Email=Email,
                                            Media_Sosial=Media_Sosial,
                                            # Deskjob
                                            Kondisi_Pekerjaan=Kondisi_Pekerjaan,
                                            Pekerjaan_Utama=Pekerjaan_Utama,
                                            Jaminan_Sosial_Ketenagakerjaan=Jaminan_Sosial_Ketenagakerjaan,
                                            Penghasilan_Sebulan_Terakhir=Penghasilan_Sebulan_Terakhir,
                                            Pengeluaran_Sebulan_Terakhir=Pengeluaran_Sebulan_Terakhir,
                                            Kepemilikan_Rumah=Kepemilikan_Rumah,
                                            Kepemilikan_Lahan_Luas=Kepemilikan_Lahan_Luas,
                                            # Deskkes
                                            Penyakit_Setahun_Terakhir=Penyakit_Setahun_Terakhir,
                                            Fasilitas_Kesehatan_Dikunjungi=Fasilitas_Kesehatan_Dikunjungi,
                                            Jumlah_Berapa_Kali_Fasilitas_Kesehatan_Dikunjungi=Jumlah_Berapa_Kali_Fasilitas_Kesehatan_Dikunjungi,
                                            Jaminan_Kesehatan_Asuransi_KIS=Jaminan_Kesehatan_Asuransi_KIS,
                                            Disabilitas=Disabilitas,
                                            # Deskpend
                                            Pendidikan_Terakhir=Pendidikan_Terakhir,
                                            Bahasa_Digunakan_Dirumah=Bahasa_Digunakan_Dirumah,
                                            Bahasa_Digunakan_Disekolah_Kantor_Tempat_Kerja=Bahasa_Digunakan_Disekolah_Kantor_Tempat_Kerja,
                                            Kerja_Bakti_Setahun_Terakhir=Kerja_Bakti_Setahun_Terakhir,
                                            Siskamling_Setahun_Terakhir=Siskamling_Setahun_Terakhir,
                                            Pesta_Rakyat_atau_Adat_Terakhir_Dilaksanakan=Pesta_Rakyat_atau_Adat_Terakhir_Dilaksanakan,
                                            Menolong_warga_Mengalami_Kematian_Setahun_Terakhir=Menolong_warga_Mengalami_Kematian_Setahun_Terakhir,
                                            Menolong_warga_Mengalami_Sakit_Setahun_Terakhir=Menolong_warga_Mengalami_Sakit_Setahun_Terakhir,
                                            Menolong_warga_Mengalami_Kecelakaan_Setahun_Terakhir=Menolong_warga_Mengalami_Kecelakaan_Setahun_Terakhir,

                                            )
                
                                                
            db.session.add(add_data_Kuisioner_Individu)

            db.session.commit()
            flash("Data Telah Dimasukkan :)")   

        user = User.query.all() 

        # Data Peta  
        Provinsi = data_peta.query.all()
    
        return render_template('forms.html', user=user, Provinsi=Provinsi)

@main.route("/tables", methods=['GET','POST'])
@login_required
def tables():
    Kuisindiv = Kuisioner_Individu.query.all()

    if request.method == 'POST' :
        edit = request.form.get('ubah')
        hapus = request.form.get('hapus')
        if edit:
            id = request.form.get('ubah')
            return redirect(url_for('homepage.forms', id=id))
        elif hapus:
            delete = Kuisioner_Individu.query.get(hapus)

            db.session.delete(delete)
            db.session.commit()
            return redirect(url_for('homepage.tables', Kuisioner_Individu=Kuisindiv))

    user = User.query.all()

    return render_template('tables.html', Kuisioner_Individu=Kuisindiv, user=user)


@main.route("/hasil_analisis")
@login_required
def hasil_analisis():
    Kuisindiv = Kuisioner_Individu.query.all()

    data = '600000'
    minus = Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita <= data)
    plus = Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita > data)

    user = User.query.all()
    return render_template('hasil_analisis.html', Kuisioner_Individu=Kuisindiv, Minus=minus, Plus=plus, user=user)


@main.route("/hasil_analisis_persentase")
@login_required
def hasil_analisis_persentase():
    Kuisindiv = Kuisioner_Individu.query.all()

    data = '600000'
    minus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita <= data).count())
    plus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita > data).count())

    # totaldatkus = Total  Data Kuisioner Individu 
    totaldatkus = Kuisioner_Individu.query.count()
    # PerKem = Persentase Kemiskinan 
    # analisis persentase pengeluaran perkapita diatas kemiskinan      
    perkemplus = plus / Kuisioner_Individu.query.count()*100
    
    # analisis persentase pengeluaran perkapita dibawah kemiskinan
    perkemminus = minus / Kuisioner_Individu.query.count()*100

    user = User.query.all()

    return render_template('hasil_analisis_persentase.html', Kuisioner_Individu=Kuisindiv, totaldatkus=totaldatkus, perkemplus=perkemplus, perkemminus=perkemminus, Minus=minus, Plus=plus, user=user)





@main.route("/input_data_shp",methods=['GET','POST'])
@main.route("/input_data_shp/<id>",methods=['GET','POST'])
@login_required
def input_data_shp(id=None):
    datapet=data_peta.query.all()
    if id :
            update=data_peta.query.filter_by(id_datapeta=id).first()
            return render_template('input_data_shp.html', row = update, id=id)
    if request.method == 'POST':
        if id :
            update=data_peta.query.filter_by(id_datapeta=id).first()
            return render_template('input_data_shp.html', row = update, id=id)
        else :
            edit = request.form.get('ubah')        
            hapus = request.form.get('hapus')        
            if edit:
                id = request.form.get('ubah')
                return redirect(url_for('homepage.input_data_shp', id=id,))
            elif hapus:
                delete = data_peta.query.get(hapus)

                db.session.delete(delete)
                db.session.commit()
                return redirect(url_for('homepage.input_data_shp', datapet=data_peta))

            Provinsi = request.form['prov']
            KotaKabupaten = request.form['kotkab']
            Kecamatan = request.form['kec']
            Desa = request.form['des']
            file = request.files['json']

            dir = 'app/static/json/temporary'
            if file:        
                namefile = file.filename
                json = "{}.json".format(namefile)

                file.save(os.path.join("app/static/json/temporary", "{}".format(namefile)))
                patoolib.extract_archive("app/static/json/temporary/{}".format(namefile), outdir="app/static/json/temporary/")

                search_shp = [f for f in os.listdir(dir) if f.endswith(".shp")]

                gjson = gpd.read_file("app/static/json/temporary/{}".format(search_shp[0]))
                gjson.to_file("app/static/json/temporary/{}".format(json), driver='GeoJSON')
                gjson = gjson.to_json()
            else:
                gjson = None

            add_Data = data_peta( Nama_File_SHP = namefile,
                                    Provinsi = Provinsi,
                                    KotaKabupaten = KotaKabupaten,
                                    Kecamatan = Kecamatan,
                                    Desa = Desa,
                                    Type_SHP = gjson)

            db.session.add(add_Data)
            db.session.commit()

            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

            flash("Data berhasil ditambahkan")

            return redirect(url_for('homepage.input_data_shp'))
# def input_data_shp():
    user = User.query.all()
    return render_template('input_data_shp.html', data_peta=datapet, user=user)



@main.route("/login")
@login_required
def login():
    return render_template('login.html')

@main.route("/register")
@login_required
def register():
    return render_template('register.html')

@main.route("/usermanager")
@login_required
def usermanager():
    user = User.query.all()
    return render_template('usermanager.html', user=user)

@ main.route("/gis", methods=['GET', 'POST'])
@ main.route("/gis/<id>", methods=['GET', 'POST'])
def gis(id=None):
    if id:
        data = data_peta.query.filter_by(id_datapeta=id).first()

        layer = gpd.read_file(data.Type_SHP)
        layer = layer.to_crs("EPSG:4326")

        m = folium.Map(location=[-1.1265694, 118.6380067],
                   zoom_start=5, min_zoom=5)

        for x in layer.index:
            color = np.random.randint(16, 256, size=3)
            # color= "green"
            color = [str(hex(i))[2:] for i in color]
            color = '#'+''.join(color).upper()
            layer.at[x, 'color'] = color

        def style(feature):
            return {
                'fillColor': feature['properties']['color'],
                'color': feature['properties']['color'],
                'weight': 1,
                'fillOpacity': 0.7
            }

        gjson = folium.GeoJson(layer, name=data.Nama_File_SHP, style_function=style).add_to(m)

        m.fit_bounds(gjson.get_bounds())

        # folium.Popup(data.desa).add_to(gjson)

        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        MousePosition(
            position="bottomleft",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Kordinat:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        tile_layer = folium.TileLayer(
            tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
            attr='google.com',
            max_zoom=19,
            name='darkmatter',
            control=False,
            opacity=1
        )
        tile_layer.add_to(m)

        m.save("app/templates/gis-maps.html")

        
        # Persentase Kemiskinan
        Kuisindiv = Kuisioner_Individu.query.all()

        data = '600000'
        minus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita <= data).count())
        plus = int(Kuisioner_Individu.query.filter(Kuisioner_Individu.Analisis_Pengeluaran_Perkapita > data).count())
        totaldatkus = Kuisioner_Individu.query.count()

        # PerKem = Persentase Kemiskinan 
        # analisis persentase pengeluaran perkapita diatas kemiskinan      
        perkemplus = plus / Kuisioner_Individu.query.count()*100
        
        # analisis persentase pengeluaran perkapita dibawah kemiskinan
        perkemminus = minus / Kuisioner_Individu.query.count()*100

        

        # Data SHP

        datapet = data_peta.query.filter_by(id_datapeta=id).first()

        return render_template("maps.html", Kuisioner_Individu=Kuisindiv, totaldatkus=totaldatkus, perkemplus=perkemplus, perkemminus=perkemminus, Minus=minus, Plus=plus, datapet=datapet, data=data, id=id)

    m = folium.Map(location=[-1.1265694, 118.6380067],
                   zoom_start=5, min_zoom=5)

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position="bottomleft",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Kordinat:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)

    tile_layer = folium.TileLayer(
        tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
        attr='google.com',
        max_zoom=19,
        name='darkmatter',
        control=False,
        opacity=1
    )
    tile_layer.add_to(m)
    
    m.save("app/templates/gis-maps.html")

    return render_template("maps.html")
