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
    ratings = []
    no_of_ratings = []
    names = []
    allRatings = db['reviews'].find()
    nameDict = {}
    countDict = {}
    for rating in allRatings:
        if rating["itemName"] in nameDict.keys():
            nameDict[rating["itemName"]] += rating["rating"]
            countDict[rating["itemName"]] += 1
        else:
            nameDict[rating["itemName"]] = rating["rating"]
            countDict[rating["itemName"]] = 1
    for k, v in nameDict.items():
        nameDict[k] = nameDict[k] / countDict[k]
    for k, v in nameDict.items():
        names.append(k)
        ratings.append(v)
        no_of_ratings.append(countDict[k])
    bayesian_rating = []
    mul_res = []
    for i in range(len(ratings)):
        mul_res.append(ratings[i] * no_of_ratings[i])
    summation = sum(mul_res)
    for i in range(len(ratings)):
        bay_adjusted_rating = ((no_of_ratings[i] * ratings[i]) + summation) / (
            no_of_ratings[i] + sum(no_of_ratings))
        bayesian_rating.append(round(bay_adjusted_rating, 1))
    for i in range(len(bayesian_rating)):
        if names[i] == itemName:
            output = bayesian_rating[i]
            count = countDict[itemName]
    return jsonify({'result': output, 'count': count})


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