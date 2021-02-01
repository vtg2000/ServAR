from flask import Flask
from flask import jsonify
from flask import request
from resources.items import items
from resources.users import users
from resources.orders import orders
from resources.reviews import reviews
from database.db import db

app = Flask(__name__)

app.register_blueprint(items)
app.register_blueprint(users)
app.register_blueprint(orders)
app.register_blueprint(reviews)

if __name__ == '__main__':
    app.run(debug=True)
