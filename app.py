# -*- coding:utf-8 -*-
# pylint: disable=E1101

import os
from flask import *
from jinja2 import FileSystemLoader
import werkzeug
from datetime import datetime
import calcImage
import io
from flask_bootstrap import Bootstrap
from hamlish_jinja import HamlishExtension
from flask_sqlalchemy import SQLAlchemy
from random import randint,choice
import battle

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 #5MB


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def topPage():
    msg = request.args.get('msg')

    loaddata = Entry.query.order_by(db.desc(Entry.id)).limit(30).all() #昇順に30件表示
    return render_template("index.html",loaddata=loaddata,msg=msg)

@app.route('/upload', methods=['POST'])
def upload_multipart():
    if 'data' not in request.files or request.form["name"]=="":
        return redirect(url_for("topPage",msg="入力に不備があります。"))
    print(request.form)
    name=request.form["name"]
    opponent_id=request.form["opponent"]
    file = request.files['data']
    print(file.filename)
    ALLOW_FILE_EXTENSION=[".jpg",".png",".JPG",".PNG",".jpeg",".JPEG"]
    if not os.path.splitext(file.filename)[1] in ALLOW_FILE_EXTENSION:
        return redirect(url_for("topPage",msg="画像はjpgとpngのみ使用できます。"))
    #opponent_load = Entry.query.order_by(db.desc(Entry.id)).limit(3).all() #昇順に5件表示
    opponent_load = db.session.query(Entry).filter_by(id=opponent_id).first()
    print("id",opponent_load.id)
    print("username",opponent_load.username)
    print("color",opponent_load.color)
    print("bp",opponent_load.battle_point)

    f = file.stream.read()
    player_color,player_BP=calcImage.run(f)
    addDatabase(name,player_color,player_BP)

    battle_result=battle.fight(player_color,player_BP,opponent_load.color,opponent_load.battle_point)
    print("result",battle_result)

    session['color']=player_color
    session['BP']=player_BP
    session['name']=name
    session["battle_result"]=battle_result

    return redirect(url_for('fighting'))

@app.route('/fighting')
def fighting():
    resultdata={
        "color":session['color'],
        "BP":session['BP'],
        "name":session['name'],
        "battle_result":session["battle_result"]
    }
    return render_template('fighting.html', resultdata=resultdata)

@app.route('/result',methods=['POST'])
def result():
    resultdata=request.form
    print(resultdata)
    return render_template('result.html', resultdata=resultdata)



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



@app.route('/ranking')
def dbPage():
    entries = Entry.query.order_by(db.desc(Entry.battle_point)).limit(30).all() #昇順に5件表示
    return render_template('db.html', entries=entries) # 変更


def addDatabase(username,color,battle_point):
    data = Entry(username=username,color=color,battle_point=battle_point)
    db.session.add(data)
    db.session.commit()

@app.route("/init_"+os.environ['INIT_KEY'])
def dbresetAndInitConfirm():
    return render_template('init.html',url="/!init_"+os.environ['INIT_KEY']) # 変更

@app.route("/!init_"+os.environ['INIT_KEY'])
def dbresetAndInit():
    Entry.query.delete()
    db.session.commit()

    text=""
    for i in range(30):
        username="名無し{0}".format(i+1)
        color=choice(["R","G","B"])
        battle_point=randint(2000,4000)
        addDatabase(username,color,battle_point)
        text+="<p>added:{0} {1} {2}</p>".format(username,color,battle_point)
        print("added:",username,color,battle_point)

    return "<p>reset ok<p>"+text
#app.debug = True
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
