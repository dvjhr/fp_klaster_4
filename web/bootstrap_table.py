from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import time

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, create_engine

host = 'localhost'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@{host}:3306/cbt_result'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

list_kota = ['', 'Bangkalan', 'Banyuwangi', 'Blitar', 'Bojonegoro', 'Bondowoso', 'Gresik', 
        'Jember', 'Jombang', 'Kediri', 'Lamongan', 'Lumajang', 'Madiun', 'Magetan', 'Malang', 
        'Mojokerto', 'Nganjuk', 'Ngawi', 'Pacitan', 'Pamekasan', 'Pasuruan','Ponorogo','Probolinggo',
        'Sampang','Sidoarjo','Situbondo','Sumenep','Trenggalek','Tuban','Tulungagung','Batu','Blitar',
        'Kediri','Madiun','Malang','Mojokerto','Pasuruan','Probolinggo','Surabaya'
        ]

def Data3(id_kota):
    print("id kota = ",id_kota)
    class Data2(db.Model):
        __tablename__ = "id_kota_"+str(id_kota)
        __table_args__ = {"extend_existing":True}

        id = db.Column(db.Integer, primary_key=True)
        id_siswa = db.Column(db.Integer)
        nama = db.Column(db.String(255))
        nrp = db.Column(db.String(255))
        id_mapel = db.Column(db.Integer)
        score = db.Column(db.Numeric(10.2))
    return Data2

data_fields = {
    'id': fields.Integer,
    'id_siswa': fields.Integer,
    'nrp': fields.String,
    'nama': fields.String,
    'id_mapel': fields.Integer,
    'score': fields.Fixed(decimals=2),
    }

# db.create_all()

def nilai_siswa(data):
    if not data:
        return None
    print('DATA MASUK', len(data))
    if type(data[0]) == type({}):
        print('DATA 1')
        nama = data[0]['nama']
        # print(nama)
        nrp = data[0]['nrp']
        # print(nrp)
        nilai = [x['score'] for x in data]

        res = {
            'nama' : nama,
            'nrp' : nrp,
            'mapel_0' : nilai[0],
            'mapel_1' : nilai[1],
            'mapel_2' : nilai[2],
            'mapel_3' : nilai[3],
            'mapel_4' : nilai[4],
            'mapel_5' : nilai[5],
            'mapel_6' : nilai[6]
        }

        print(res)
        return res
    elif type(data[0][0]) == type({}):
        print('DATA 2', data[0][0])
        for i in range(0, len(data)):
            nilai_siswa(data[i])

def all_result(result):
    ls = []
    rem = len(result) // 7
    a = 0
    # print(result)
    for i in range(7, rem * 7 + 1, 7):
        ls.append(nilai_siswa(result[a:i]))
        a += 7
    result = ls
    return result
    

@app.route('/')
def index():
    print('MASUK SEMUA')
    url = f'http://{host}:5000/'
    users = requests.get(url=url).json()
    # print('INI HASIL PRINT WOYYY', users)
    users = all_result(users[0])
    print('INI HASIL PRINT WOYYY', type(users), len(users))
    return render_template('bootstrap_table.html', title='Bootstrap Table', data=users, kota=list_kota)

@app.route('/siswa/nrp/<string:siswa_nrp>')
def func_nrp(siswa_nrp):
    print('MASUK NRP')
    url = f'http://{host}:5000/siswa/nrp/'+str(siswa_nrp)
    if requests.get(url=url).status_code == 404:
        return render_template('bootstrap_table.html', title=f'Data Not Found', data=[], kota=[])
    users = requests.get(url=url).json()
    # print(users)
    print('USERS', len(users))
    if (len(users[0]) == 7):
        all_users = []
        for i in range(0, len(users)):
            # all_result(users[i])[0]
            all_users.append(all_result(users[i])[0])
        users = all_users
    else:
        users = all_result(users)
    return render_template('bootstrap_table.html', title=f'Show all Siswa which NRP is {siswa_nrp}', data=users, kota=list_kota)

@app.route('/siswa/nama/<string:siswa_nama>')
def func_nama(siswa_nama):
    print('MASUK NAMA', siswa_nama)
    url = f'http://{host}:5000/siswa/nama/'+str(siswa_nama)
    if requests.get(url=url).status_code == 404:
        return render_template('bootstrap_table.html', title=f'Data Not Found', data=[], kota=[])
    users_raw = requests.get(url=url).json()
    # print(users_raw)
    users = all_result(users_raw[0])
    return render_template('bootstrap_table.html', title=f'Show all Siswa which Nama contains \'{siswa_nama}\'', data=users, kota=list_kota)

@app.route('/siswa/kota/<int:id_kota>')
def func_kota(id_kota):
    print('MASUK KOTA', id_kota)
    if int(id_kota) == 0:
        print('MASUK 0')
        return index()
    url = f'http://{host}:5000/siswa/kota/'+str(id_kota)
    if requests.get(url=url).status_code == 404:
        return render_template('bootstrap_table.html', title=f'Data Not Found', data=[], kota=[])
    users = requests.get(url=url).json()
    users = all_result(users)
    # print(users)
    return render_template('bootstrap_table.html', title=f'Show all Siswa within Kota {list_kota[int(id_kota)]}', data=users, kota=list_kota)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        print('MASUK SEARCH')
        nama = request.form.get('nama', False)
        nrp = request.form.get('nrp', False)
        kota = request.form.get('kota', False)

    if nama:
        return func_nama(nama)
    elif nrp:
        return func_nrp(nrp)
    elif kota:
        return func_kota(kota)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
