#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    """Return a list of all bakeries."""
    bakeries = Bakery.query.all()
    bakery_list = []
    for b in bakeries:
        bakery_list.append(b.to_dict())

    response = make_response(
        bakery_list,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    """Return the details of a single bakery by its ID."""
    target_bakery = Bakery.query.get(id)
    if target_bakery:
        return make_response(target_bakery.to_dict(), 200)
    else:
        return make_response({"Error":"The Bakery with that ID was not found"}, 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    my_baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
  
    baked_list = []

    for baked_good in my_baked_goods:
        baked_list.append(baked_good.to_dict())

    response = make_response(
        baked_list,
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if baked_good:
        return make_response(
            baked_good.to_dict(),
            200
        )
    else:
        return make_response({"Error":"The baked food is not found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
