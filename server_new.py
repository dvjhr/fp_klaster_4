from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, create_engine
import time

app = Flask(__name__)
api = Api(app)
# Format: mysql://[username]:[password]@[host]:[port]/[database]'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost:3306/cbt_result'
# ses = sessionmaker()
# session = ses()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = Session(engine, future=True)

jumlah_siswa = 50
limit = jumlah_siswa * 7

db = SQLAlchemy(app)

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

# @api.resource('/siswa/', '/siswa/<int:siswa_nrp>')
# @api.resource('/siswa/int:<id_kota>/<int:siswa_nrp>')
@api.resource('/', '/siswa/nrp/<siswa_nrp>', '/siswa/<int:id_kota>/<int:siswa_nrp>', '/siswa/nama/<string:siswa_nama>', '/siswa/kota/<int:id_kota>')
class Data_Resource(Resource):
    @marshal_with(data_fields)
    def get(self, id_kota=None, siswa_nrp=None, siswa_nama=None):
        result = []
        tAll = time.time()
        print(bool(id_kota), bool(siswa_nrp), bool(siswa_nama))
        if id_kota:
            print("Masuk KOTA")
            Data = Data3(id_kota)
            if not siswa_nrp:
                print("Masuk SEMUA")
                result = Data.query.limit(limit).all()
            elif siswa_nrp:
                print("Masuk NRP 1")
                result = Data.query.filter_by(nrp=siswa_nrp).limit(limit).all()
        
        elif not id_kota:
            if siswa_nrp:
                print("Masuk NRP 2", type(siswa_nrp), siswa_nrp)
                id_kota = 1
                result_all = []
                while id_kota < 38:
                    Data = Data3(id_kota)
                    if siswa_nrp:
                        result = session.query(Data).filter(Data.nrp.ilike(f'%{siswa_nrp}%')).limit(limit).all()
                        # print(result)
                    result_all.append(result)
                    id_kota += 1
                print('PANJANG', len(result_all))
                result = result_all
            elif siswa_nama:
                print("Masuk NAMA")
                id_kota = 1
                result_all = []
                while id_kota < 39:
                    Data = Data3(id_kota)
                    if siswa_nama:
                        result = session.query(Data).filter(Data.nama.ilike('%'+siswa_nama+'%')).limit(limit).all()
                    result_all.append(result)
                    id_kota += 1
                result = result_all
                print(result)
        if not id_kota and not siswa_nrp and not siswa_nama:
            print("masuk else")
            print("Masuk SEMUA")
            result = []
            ab = 0
            for i in range (1,39):
                Data = Data3(i)
                result_once = Data.query.limit(limit).all()
                for a in result_once:
                    # print(ab+1, a.nrp)
                    ab += 1
                
                result.append(result_once)

        # print(type(result))
        # print(result)
        elapsed = time.time() - tAll
        print(f"Jumlah Data: {len(result)}")
        print("Time selesai  = {:.3f}s".format(elapsed))

        if type(result) == type([]) and  type(result[0]) == type([]):
            if len(result) == 0 or len(result[0]) == 0:
                abort(404, message=f"Data tidak ditemukan")
        return result

if __name__ == "__main__":
    app.run(port=5000, debug=True)