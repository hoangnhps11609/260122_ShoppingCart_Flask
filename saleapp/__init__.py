from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = 'asdfghjkl'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345678@localhost/saleDB?charset="

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Shopping', template_mode='bootstrap4')