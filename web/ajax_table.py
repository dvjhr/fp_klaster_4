from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost:3306/cbt_result'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

# db.create_all()


@app.route('/')
def index():
    print("cwd=", os.getcwd())
    return render_template('ajax_table.html', title='Ajax Table')

# 
# @app.route('/api/data')
# def data():
#     return {'data': [user.to_dict() for user in User.query]}


if __name__ == '__main__':
    app.run(port=5001, debug=True)