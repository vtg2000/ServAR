from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db

users = Blueprint('users', __name__)


@users.route('/api/users')
def getNewUserId():
    appUsers = db.users.find()
    return jsonify({'newUserId': appUsers.count() + 1})


@users.route('/api/users/<id>', methods=['GET'])
def getUser(id):
    output = []
    appUsers = db.users.find({"userId": int(id)})
    for user in appUsers:
        output.append({
            'userId': user['userId'],
            'username': user['username'],
            'phone': user['phone']
        })
    return jsonify({'result': output})


@users.route('/api/users', methods=['POST'])
def postUser():
    appUsers = db.users
    username = request.json['username']
    userId = request.json['userId']
    phone = request.json['phone']
    newUserId = appUsers.insert({
        'username': username,
        'userId': userId,
        'phone': phone
    })
    newUser = appUsers.find_one({'_id': newUserId})
    output = {
        'username': newUser['username'],
        'userId': newUser['userId'],
        'phone': newUser['phone']
    }

    return jsonify({'result': output, "outcome": "Success"})
