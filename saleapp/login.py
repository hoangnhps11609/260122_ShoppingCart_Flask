from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response

from flask_mysqldb import MySQL

import MySQLdb.cursors

import re

import jwt
from datetime import datetime, timedelta
from functools import wraps
from saleapp import app, db

mysql = MySQL(app)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'token': 'token is missing'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'alert': 'invalid token'})
    return decorated

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            token = jwt.encode({
                'user': request.form['username'],
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
            },
                app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('utf-8')})
            msg = 'Logged in successfully !'
            return msg
        else:
            msg = 'Incorrect username / password !'
    return msg
