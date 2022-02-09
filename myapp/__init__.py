
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hgny/Desktop/Python/JWT_API_Cart/cart.db'

db = SQLAlchemy(app)