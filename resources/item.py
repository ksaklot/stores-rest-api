from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type= float,
    required = True,
    help = "This field can not be left blank"
    )

    parser.add_argument('store_id',
    type= float,
    required = True,
    help = "Every item needs a store id"
    )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        #item = next(filter(lambda x : x['name'] == name, items), None)
        return {'message': 'item not found'}, 404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201


    def delete(self,name):
        #global items
        #items = list(filter(lambda x: x['name'] == name, items))
        item = ItemModel.find_by_name(name)
        if item:
            item.update()

        return {'message': 'item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
        #item = next(filter(lambda x : x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'],data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()] }
