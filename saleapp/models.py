from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from saleapp import db

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    price = Column(Float, nullable=False)
    cartItem = relationship('CartItem', backref="product", lazy=True)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subtotal = Column(Float)
    total = Column(Float)
    vat = Column(Integer)
    cartItem = relationship('CartItem', backref="cart", lazy=True)
    userId = db.Column(Integer, ForeignKey('user.id'), nullable=False)

class CartItem(db.Model):
    __tablename__ = 'cartItem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    quantity = Column(Integer, default= 1)
    subtotal = Column(Float)
    productId = db.Column(Integer, ForeignKey(Product.id), nullable=False)
    cartId = db.Column(Integer, ForeignKey('cart.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(45), nullable=False)
    lastName = Column(String(45), nullable=False)
    userName = Column(String(45), nullable=False)
    password = Column(String(10), nullable=False)
    email = Column(String(45), nullable=False)
    cartId = relationship("Cart", uselist=False, backref="user")

if __name__ == "__main__":
    db.create_all()
