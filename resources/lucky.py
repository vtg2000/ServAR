from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db
import datetime
import calendar
import operator

lucky = Blueprint('lucky', __name__)


@lucky.route('/api/lucky')
def getLuckyItems():
    output = []
    items = db['lucky'].find()
    print(datetime.datetime.now())
    now = datetime.datetime.now()
    currentHour = now.hour
    today = calendar.day_name[now.today().weekday() - 1].lower() + "Score"
    mealType = ""
    scores = []
    if currentHour > 6 and currentHour < 12:
        mealType = "breakfastScore"
    elif currentHour < 16:
        mealType = "lunchScore"
    elif currentHour < 20:
        mealType = "snackScore"
    elif currentHour < 24 or currentHour < 6:
        mealType = "dinnerScore"
    for item in items:
        name = item['itemName']
        score = item[mealType] + item[today] + item['popularityScore']
        scores.append([name, score])
    scores = sorted(scores, key=operator.itemgetter(1), reverse=True)
    for i in range(3):
        output.append(scores[i][0])
    return jsonify({'result': scores, "output": output})


@lucky.route('/api/preferences/<userId>')
def getPreferencesForUser(userId):
    output = []
    orders = db['orders'].find({"userid": (userId)})
    itemDict = {}
    for order in orders:
        for item in order['items']:
            if item['itemName'] not in itemDict.keys():
                itemDict[item['itemName']] = item['itemQuantity']
            else:
                itemDict[item['itemName']] += item['itemQuantity']
    itemDict = sorted(itemDict.items(),
                      key=operator.itemgetter(1),
                      reverse=True)
    for k, v in itemDict:
        output.append(k)
    output = output[:3]
    itemDict = itemDict[:3]
    return jsonify({"result": itemDict, "output": output})
