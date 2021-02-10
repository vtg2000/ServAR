from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db
import datetime
import calendar
import operator
import pymongo

orders = Blueprint('orders', __name__)


@orders.route('/api/orders')
def getAllOrders():
    output = []
    orders = db['orders'].find()
    for order in orders:
        output.append({
            'items': order['items'],
            'orderid': order['orderid'],
            'timestamp': order['timestamp'],
            'orderETA': order['orderETA'],
            'orderAmount': order['orderAmount'],
            'delivered': order['delivered']
        })
    return jsonify({'result': output})


@orders.route('/api/orders/<userId>')
def getOrdersByUser(userId):
    output = []
    orders = db['orders'].find({
        "userid": userId
    }).sort('timestamp', pymongo.DESCENDING)
    for order in orders:
        output.append({
            '_id': str(order['_id']),
            'orderid': order['orderid'],
            'items': order['items'],
            'timestamp': order['timestamp'],
            'orderETA': order['orderETA'],
            'orderAmount': order['orderAmount'],
            'delivered': order['delivered']
        })
    return jsonify({'result': output})


@orders.route('/api/orders/order/<orderid>')
def getOrdersByOrderId(orderid):
    output = []
    orders = db['orders'].find({
        "orderid": int(orderid)
    }).sort('timestamp', pymongo.DESCENDING)
    for order in orders:
        output.append({
            '_id': str(order['_id']),
            'orderid': order['orderid'],
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
            output = max(output, order['orderETA'] - offset)
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
        'orderid': db.orders.count_documents({}) + 1,
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

    lucky = db.lucky
    now = datetime.datetime.now()
    currentHour = now.hour
    today = calendar.day_name[now.today().weekday()].lower() + "Score"
    mealType = ""
    if currentHour > 6 and currentHour < 12:
        mealType = "breakfastScore"
    elif currentHour < 16:
        mealType = "lunchScore"
    elif currentHour < 20:
        mealType = "snackScore"
    elif currentHour < 24 or currentHour < 6:
        mealType = "dinnerScore"

    for item in items:
        luckyItem = lucky.find_one({"itemName": item['itemName']})
        lucky.update_one({"itemName": item['itemName']}, {
            "$set": {
                today:
                luckyItem[today] + 0.3 * item['itemQuantity'],
                mealType:
                luckyItem[mealType] + 0.5 * item['itemQuantity'],
                "popularityScore":
                luckyItem["popularityScore"] + 1 * item['itemQuantity']
            }
        },
                         upsert=True)

    return jsonify({'result': output, "outcome": "Success"})