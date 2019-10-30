# pylint: disable=E1101

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask import * #Flask,make_response,render_template,request, jsonify,g,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from random import choice,randint
import os

app = Flask(__name__)
db_uri = os.environ['DATABASE_URL'] # 追加
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri # 追加
db = SQLAlchemy(app) # 追加


class Entry(db.Model): # 追加
    __tablename__ = "userdata" # 追加
    USERDATA_ID_SEQ = db.Sequence('userdata_id_seq')
    id = db.Column(db.Integer,USERDATA_ID_SEQ, primary_key=True,server_default=USERDATA_ID_SEQ.next_value()) # 追加
    username = db.Column(db.String(), nullable=False) # 追加
    color = db.Column(db.String(1), nullable=False) # 追加
    battle_point = db.Column(db.Integer, nullable=False) # 追加


def addDatabase(username,color,battle_point):
    data = Entry(username=username,color=color,battle_point=battle_point)
    db.session.add(data)
    db.session.commit()


def initDatabase():
    record_count=int(input("レコードの数："))
    bp_range=input("BPの範囲 (例)1500,3000　：").split(",")
    if len(bp_range)!=2:
        print("正しく入力してください")
    input("Enterで開始")
    for i in range(record_count):
        username="名無し{0}".format(i)
        color=choice(["R","G","B"])
        battle_point=randint(int(bp_range[0]),int(bp_range[1]))
        addDatabase(username,color,battle_point)
        print("added:",username,color,battle_point)
if __name__ == "__main__":
    initDatabase()
