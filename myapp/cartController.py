
from flask import request, jsonify
import uuid

from data.models import Cart, CartItem, Product
from myapp import db, app
from myapp.token import token_required

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
    cart.subtotal = subtotal
    cart.total = subtotal + (subtotal/cart.vat)
    db.session.commit()
    cartlist = {}
    cartlist['id'] = cart.id
    cartlist['subtotal'] = subtotal
    cartlist['total'] = subtotal + (subtotal/cart.vat)
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
