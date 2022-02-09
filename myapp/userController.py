
from flask import request, jsonify
import uuid
from werkzeug.security import generate_password_hash

from data.models import User, Cart
from myapp import db, app
from myapp.token import token_required



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
