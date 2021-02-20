from flask import Blueprint
from flask import jsonify
from flask import request
from database.db import db

nutrition = Blueprint('nutrition', __name__)


@nutrition.route('/api/nutrition/<itemName>')
def getNutritionByItemName(itemName):
    output = []
    nutritions = db['nutrition'].find({"item": itemName})
    for nutrition in nutritions:
        output.append({
            'energy': nutrition['energy'],
            'protein': nutrition['protein'],
            'fat': nutrition['fat'],
            'carbs': nutrition['carbs'],
        })
    return jsonify({'result': output})