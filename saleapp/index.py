
from flask import Flask, render_template, request, session, jsonify
import jwt
from saleapp import app, db
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from datetime import datetime , timedelta
from functools import wraps
from saleapp.admin import *


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs) :
        token = request.args.get('token')
        if not token:
            return jsonify({'token':'token is missing'})
        try:
            payload = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'alert':'invalid token'})
    return decorated


@app.route('/public')
def public():
    return 'for public'

@app.route('/auth')
@token_required
def auth():
    return 'jwt is verified'



# @saleapp.route("/")
# def home():
#     return render_template('index.html')


#path params
#khong kieu la string
# @saleapp.route("/<int:name>")
# def home(name):
#     return render_template('index.html', message= "Xin chao %d" %name)

#getparam
# @saleapp.route("/test")
# def home():
#     fn = request.args.get('first_name', 'Auto')
#     ln = request.args.get('last_name', 'Auto')
#     return render_template('index.html', message= "Xin chao %s %s" %(fn, ln))
#
# @app.route("/")
# def home():
#     users = [{
#         "name" : "Hoang",
#         "email" : "hoang@gmail.com"
#     },{
#         "name": "Tien",
#         "email": "tien@gmail.com"
#     },{
#         "name": "Ki",
#         "email": "ki@gmail.com"
#     }]
#
#     kw = request.args.get("keyword")
#     if kw:
#         users = [u for u in users if u['name'].lower().find(kw.lower()) >= 0]
#     return render_template('index.html', users=users)
#

# @app.route("/login", methods=['post'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#     if username =='admin' and password =='123':
#         return "success"
#     return "failed"

@app.route("/upload", methods=['post'])
def upload():
    f = request.files['avatar']
    f.save(os.path.join(app.root_path, 'static/uploads', f.filename))
    return 'Done'




if __name__ == "__main__":
    app.run(debug=True)