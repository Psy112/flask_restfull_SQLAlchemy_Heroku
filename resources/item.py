from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import ItemModel


class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('price',
                       type=float,
                       required=True,
                       help="price can't be left blank !!"
                       )
    parse.add_argument('store_id',
                       type=int,
                       required=True,
                       help="item must have a store !!"
                       )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {"message": "item doesn't exist"}, 404  # ERROR CODE FOR NOT FOUND , 200 CODE FOR OK

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "item {} already exist".format(name)}, 400  # ERROR CODE

        data = Item.parse.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": "item {} not found".format(name)}, 400  # ERROR CODE

        item.delete()
        return {"message": "item {} was deleted".format(name)}, 200

    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel(name, **data)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
