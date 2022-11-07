import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.secret_key = "massin"  # ENCRYPT/DECRYPT DATA
api = Api(app)




jwt = JWT(app, authenticate, identity)  # JWT create an endpoint /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, "/register")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == "__main__":
    from db import db  # SERT À ÉVITER UN IMPORT CIRCULAIRE

    db.init_app(app)
    app.run(port=5000, debug=True)
