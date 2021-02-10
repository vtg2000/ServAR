from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db
import datetime
import pymongo

reviews = Blueprint('reviews', __name__)


@reviews.route('/api/reviews')
def getAllReviews():
    output = []
    reviews = db['reviews'].find()
    for review in reviews:
        output.append({
            'username': review['username'],
            'itemName': review['itemName'],
            'rating': review['rating'],
            'review': review['review'],
            'timestamp': review['timestamp']
        })
    return jsonify({'result': output})


@reviews.route('/api/reviews/<userId>')
def getReviewsByUser(userId):
    output = []
    reviews = db['reviews'].find({"userId": int(userId)})
    for review in reviews:
        output.append({
            'username': review['username'],
            'itemName': review['itemName'],
            'rating': review['rating'],
            'review': review['review'],
            'timestamp': review['timestamp']
        })
    return jsonify({'result': output})


@reviews.route('/api/reviews/item/<itemName>')
def getReviewsForItem(itemName):
    output = []
    reviews = db['reviews'].find({
        "itemName": itemName
    }).sort('timestamp', pymongo.DESCENDING)
    for review in reviews:
        output.append({
            'username': review['username'],
            'itemName': review['itemName'],
            'rating': review['rating'],
            'review': review['review'],
            'timestamp': review['timestamp']
        })
    return jsonify({'result': output})


@reviews.route('/api/ratings/item/<itemName>')
def getRatingsForItem(itemName):
    rating = 0
    count = 0
    reviews = db['reviews'].find({"itemName": itemName})
    for review in reviews:
        count += 1
        rating += review['rating']
    if rating == 0:
        output = 4.5
    else:
        # can apply any rating algo here, for now its plain average
        output = rating / count
    return jsonify({'result': output})


@reviews.route('/api/reviews', methods=['POST'])
def postReview():
    reviews = db.reviews
    userId = request.json['userId']
    username = request.json['username']
    timestamp = datetime.datetime.now()
    rating = request.json['rating']
    review = request.json['review']
    itemName = request.json['itemName']
    newReviewId = reviews.insert({
        'username': username,
        'userId': userId,
        'rating': rating,
        'review': review,
        'itemName': itemName,
        'timestamp': datetime.datetime.now()
    })
    newReview = reviews.find_one({'_id': newReviewId})
    output = {
        'username': newReview['username'],
        'userId': newReview['userId'],
        'rating': newReview['rating'],
        'review': newReview['review'],
        'itemName': newReview['itemName'],
        'timestamp': newReview['timestamp']
    }
    return jsonify({'result': output, "outcome": "Success"})