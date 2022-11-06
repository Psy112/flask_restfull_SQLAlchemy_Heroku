from flask_restful import Resource
from models import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel(name)
        if store.find_by_name(name):
            return store.json()
        return {"message": "store not found"}, 404

    def post(self, name):
        if StoreModel(name).find_by_name(name):
            return {"message": f"store {name} already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "internal error"}, 500

        return store.json(), 201

    def delete(self, name):
        if not StoreModel(name).find_by_name(name):
            return {"message": "store doesn't exist"}, 404

        store = StoreModel(name)

        try:
            store.delete_from_db()
        except:
            return {"message": "internal error"}, 500

        return {"message": f"store {name} was deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
