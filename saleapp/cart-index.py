from random import random

from flask import Flask, jsonify

import utils

app = Flask(__name__)

@app.route("/cart", methods=["GET"])
def get_cart():
    rows = utils.get_Item("Select * from cartItem")
    data=[]
    for r in rows:
        data.append({
            "id": r[0],
            "productId": r[1],
            "price": r[2],
            "quantity": r[3],
            "subtotal": r[4]
        })
    return jsonify({"cartItem": data})

@app.route("/cartItem/<product_id>/<int:quantity>", methods=["POST"])
def add_product(product_id, quantity):
    n = random.randint(0, 9999)
    utils.add_Item_in_Cart(random, product_id, quantity)
    rows = utils.get_Item("Select * from cartItem")
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "productId": r[1],
            "price": r[2],
            "quantity": r[3],
            "subtotal": r[4]
        })
    return jsonify({"cartItem": data})

@app.route("/cartItem", methods=["PUT"])
def updateQuantity():
    pass

@app.route("/cartItem", methods=["DELETE"])
def deleteItem():
    pass

if __name__ == "__main__":
    app.run()