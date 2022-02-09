
from flask import request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from data.models import User, Cart, CartItem, Product
from myapp import db, app
from myapp.token import token_required


#
#
# app = Flask(__name__)
#
# app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hgny/Desktop/Python/JWT_API_Cart/cart.db'
#
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     name = db.Column(db.String(50))
#     password = db.Column(db.String(80))
#
# class Product(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     name = db.Column(db.String(50))
#     price = db.Column(db.Float)
#
# class Cart(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     subtotal = db.Column(db.Float)
#     total = db.Column(db.Float)
#     vat = db.Column(db.Integer)
#
# class CartItem(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     price = db.Column(db.Float)
#     subtotal = db.Column(db.Float)
#     quantity = db.Column(db.Integer)
#     cartId = db.Column(db.String(50))
#     productId = db.Column(db.String(50))
#
#
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#
#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401
#
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(id=data['id']).first()
#         except:
#             return jsonify({'message' : 'Token is invalid!'}), 401
#
#         return f(current_user, *args, **kwargs)
#
#     return decorated



@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perforn that function!'})

    users = User.query.all()
    output = []
    print(current_user)
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users' : output})

@app.route('/user/<id>', methods=['GET'])
@token_required
def get_one_user(current_user, id):
    if not current_user:
        return jsonify({'message': 'Cannot perforn that function!'})

    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message' : 'no user found' })
    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['password'] = user.password
    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perforn that function!'})
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    uid = str(uuid.uuid4())
    new_user = User(id = uid, name=data['name'], password=hashed_password)
    cart_for_new_user = Cart(id =uid, subtotal =0, total=0, vat=10)
    db.session.add(new_user)
    db.session.add(cart_for_new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created'})

@app.route('/user/<id>', methods=['PUT'])
@token_required
def promote_user(current_user, id):
    if not current_user:
        return jsonify({'message': 'Cannot perforn that function!'})
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'no user found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    if not current_user:
        return jsonify({'message': 'Cannot perforn that function!'})
    user = User.query.filter_by(id=id).first()
    cart = Cart.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'no user found'})
    db.session.delete(user)
    db.session.delete(cart)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted'})

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/items', methods=['GET'])
@token_required
def get_all_items(current_user):
    cartItems = CartItem.query.filter_by(cartId=current_user.id).all()
    output = []
    for cartItem in cartItems:
        list = {}
        list['id'] = cartItem.id
        list['price'] = cartItem.price
        list['quantity'] = cartItem.quantity
        list['subtotal'] = cartItem.subtotal
        list['productId'] = cartItem.productId
        list['cartId'] = cartItem.cartId
        output.append(list)
    return jsonify({'cartItem' : output})





@app.route('/cartInfo', methods=['GET'])
@token_required
def get_cartInfo(current_user):
    cart = Cart.query.filter_by(id=current_user.id).first()
    if not cart:
        return jsonify({'message' : 'no cart found'})

    cartItems = CartItem.query.filter_by(cartId=current_user.id).all()

    subtotal = 0.0
    for cartItem in cartItems:
        subtotal += cartItem.subtotal
    cartlist = {}
    cartlist['id'] = cart.id
    cartlist['subtotal'] = subtotal
    cartlist['total'] = subtotal - (subtotal/cart.vat)
    cartlist['vat'] = cart.vat
    return jsonify(cartlist)

@app.route('/items/<productId>', methods=['POST'])
@token_required
def add_items(current_user, productId):
    product = Product.query.filter_by(id=productId).first()
    if not product:
        return jsonify({'message': 'no product found'})
    productInCartItem = CartItem.query.filter_by(productId=productId, cartId=current_user.id).first()
    if productInCartItem:
        productInCartItem.quantity = productInCartItem.quantity + 1
        productInCartItem.subtotal = productInCartItem.subtotal + productInCartItem.price
        db.session.commit()
        return jsonify({'message': "Product +1 to cart"})
    else:
        data = request.get_json()
        new_todo = CartItem(id=str(uuid.uuid4()), price=product.price, quantity=data['quantity'], subtotal=product.price*data['quantity'], productId = productId, cartId= current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'message' : "Product add to cart"})

@app.route('/updatecartItem/<id>', methods=['PUT'])
@token_required
def updateCartItem(current_user, id):
    cartItem = CartItem.query.filter_by(id=id).first()
    if not cartItem:
        return jsonify({'message': 'no cartItem found'})
    data = request.get_json()
    cartItem.quantity = data['quantity']
    cartItem.subtotal = cartItem.price * data['quantity']
    db.session.commit()
    return jsonify({'message': "cart Item updated"})

@app.route('/deletecartItem/<id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, id):
    cartItem = CartItem.query.filter_by(id=id).first()
    if not cartItem:
        return jsonify({'message': 'no cartItem found'})
    db.session.delete(cartItem)
    db.session.commit()
    return jsonify({'message': "Product was deleted in cartS"})

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=5001)