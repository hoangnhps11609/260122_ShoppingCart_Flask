import requests as requests
from flask import request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash
import hashlib
from data.models import User, Cart, Order, CartItem
from myapp import db, app
from myapp.token import token_required

@app.route('/order', methods=['POST'])
@token_required
def create_order(current_user):
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})
    cart = Cart.query.filter_by(id=current_user.id).first()
    cartItems = CartItem.query.filter_by(cartId=current_user.id).all()
    if not cart:
        return jsonify({'message': 'no cart found'})
    data = request.get_json()
    orderId = str(uuid.uuid4())
    merchantId = data['merchantId']
    amount = cart.total
    signature = hashlib.md5((merchantId+str(amount)+orderId).encode()).hexdigest()
    create_order = Order(id=orderId, amount=amount, merchantId=merchantId, signature=signature, status="Waiting Confirm")
    db.session.add(create_order)
    cart.total = 0.0
    cart.subtotal = 0.0
    for item in cartItems:
        db.session.delete(item)
        db.session.commit()
    db.session.commit()

    order = Order.query.filter_by(id=orderId).first()
    order_data = {}
    order_data['id'] = order.id
    order_data['amount'] = order.amount
    order_data['merchantId'] = order.merchantId
    order_data['signature'] = order.signature
    order_data['status'] = order.status
    return jsonify({'order': order_data})


@app.route('/getOrder/<id>', methods=['POST'])
def getOrder(id):
    order = Order.query.filter_by(id=id).first()
    order_data = {}
    order_data['id'] = order.id
    order_data['amount'] = order.amount
    order_data['merchantId'] = order.merchantId
    order_data['signature'] = order.signature
    order_data['status'] = order.status
    return jsonify({'order': order_data})


@app.route('/checkout/<id>', methods=['POST'])
@token_required
def payMent(current_user, id):
    if not current_user:
        return jsonify({'message': 'Cannot perform that function!'})

    order = Order.query.filter_by(id=id).first()
    if order.status != "Waiting Confirm":
        return jsonify({'message': 'Order comfirmed'})
    data = {
        'merchantId': 'd56607b9-c96a-43b9-bd82-2d0bb3ca8762',
        'amount': order.amount,
        'extraData': order.id,
        'signature': order.signature
    }
    r = requests.post("http://127.0.0.1:5006/transaction/create", data=data)
    order.status = 'Confirmed'
    db.session.commit()
    return make_response(jsonify({
                'status': 'success',
                'data': data
            })), 201


@app.route('/order/updateStatus', methods=['POST'])
def updateStatus():
    data = request.form.to_dict()
    order = Order.query.filter_by(id=data['extraData']).first()
    if not order:
        return jsonify({'message': 'no order found'})
    order.status = data['status']
    db.session.commit()
    return make_response(jsonify({
        'status': 'success'
    })), 201