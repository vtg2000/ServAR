from flask import Blueprint
from flask import jsonify
from database.db import db

items = Blueprint('items', __name__)


@items.route('/api/items')
def getItems():
    output = []
    items = db['items'].find()
    for item in items:
        output.append({
            'itemName': item['itemName'],
            'itemETA': item['itemETA'],
            'itemPrice': item['itemPrice']
        })
    return jsonify({'result': output})


@items.route('/api/items/<itemName>')
def getItem(itemName):
    output = []
    items = db['items'].find({"itemName": itemName})
    for item in items:
        output.append({
            'itemName': item['itemName'],
            'itemETA': item['itemETA'],
            'itemPrice': item['itemPrice']
        })
    return jsonify({'result': output})