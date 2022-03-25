# 6A / 19090052 / Akhmad Ali Husni Fauzan
# 6A / 19090002 / M. Ade Noval Firmansyah

import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "jawaban.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
    keterangan = db.Column(db.String(150))
    
@app.route("/api/v1/login", methods=["POST"])
def login():
    username= request.form['username']
    password= request.form['password']
    S=10
    user=User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        user.token= token
        db.session.commit()
    return jsonify({
        "msg": "Login Berhasil",
        "status": 200,
        "token": token,
    })
@auth.verify_token
def verify_token(token):
    user=User.query.filter_by(token=token).first() 
    return user.keterangan 
@app.route("/api/v2/users/info", methods=["POST"])
@auth.login_required
def info():
    return "Hai, {}!".format(auth.current_user())
if __name__ == '__main__':
    app.run(debug = True, port=4000)