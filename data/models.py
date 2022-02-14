from myapp import db

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))

class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)

class Cart(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    subtotal = db.Column(db.Float)
    total = db.Column(db.Float)
    vat = db.Column(db.Integer)

class CartItem(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    price = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    cartId = db.Column(db.String(50))
    productId = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    amount = db.Column(db.Float)
    merchantId = db.Column(db.String(50))
    signature = db.Column(db.String(50))
    status = db.Column(db.String(50))