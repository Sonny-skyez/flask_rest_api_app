from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import autnenticate, identity


app = Flask(__name__)
app.secret_key = "Kris"
api = Api(app)

jwt = JWT(app, autnenticate, identity)  # /auth

items = []


class Item(Resource):
    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)

        return {"item": item}, 200 if item else 404

    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": "Item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item with name '{}' deleted.".format(name)}

    # @jwt_required()
    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5001, debug=True)

a = 0
