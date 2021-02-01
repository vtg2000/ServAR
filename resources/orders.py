from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db
import datetime

orders = Blueprint('orders', __name__)


@orders.route('/api/orders')
def getAllOrders():
    output = []
    orders = db['orders'].find()
    for order in orders:
        output.append({
            'items': order['items'],
            'timestamp': order['timestamp'],
            'orderETA': order['orderETA'],
            'orderAmount': order['orderAmount'],
            'delivered': order['delivered']
        })
    return jsonify({'result': output})


@orders.route('/api/orders/<userId>')
def getOrdersByUser(userId):
    output = []
    orders = db['orders'].find({"userid": int(userId)})
    for order in orders:
        output.append({
            'items': order['items'],
            'timestamp': order['timestamp'],
            'orderETA': order['orderETA'],
            'orderAmount': order['orderAmount'],
            'delivered': order['delivered']
        })
    return jsonify({'result': output})


@orders.route('/api/pendingETA')
def getPendingEta():
    output = 0
    orders = db['orders'].find({"delivered": False})
    now = datetime.datetime.now()
    fmt = "%d-%m-%Y %H:%M:%S"
    for order in orders:
        offset = int((now - order['timestamp']).total_seconds() / 60.0)
        if offset >= order['orderETA']:
            db['orders'].update_one({"_id": order["_id"]},
                                    {"$set": {
                                        "delivered": True
                                    }},
                                    upsert=True)
        else:
            output += order['orderETA'] - offset
    return jsonify({'result': output})


@orders.route('/api/orders', methods=['POST'])
def postOrder():
    orders = db.orders
    userid = request.json['userid']
    timestamp = datetime.datetime.now()
    items = request.json['items']
    orderETA = request.json['orderETA']
    orderAmount = request.json['orderAmount']
    delivered = False
    newOrderId = orders.insert({
        'userid': userid,
        'items': items,
        'timestamp': timestamp,
        'orderETA': orderETA,
        'orderAmount': orderAmount,
        'delivered': delivered
    })
    newOrder = orders.find_one({'_id': newOrderId})
    output = {
        'userid': newOrder['userid'],
        'items': newOrder['items'],
        'timestamp': newOrder['timestamp'],
        'orderETA': newOrder['orderETA'],
        'orderAmount': newOrder['orderAmount'],
        'delivered': newOrder['delivered']
    }

    return jsonify({'result': output, "outcome": "Success"})