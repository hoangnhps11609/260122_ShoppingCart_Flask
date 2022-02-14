from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hgny/Desktop/Python/JWT_API_Cart/cart.db'

db = SQLAlchemy(app)

from myapp import cartController
from myapp import userController
from myapp import orderController
from myapp import login
