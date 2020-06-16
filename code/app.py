import os

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.item import ItemModel


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Kris"
api = Api(app)


@app.route("/")
def render_index_html():
    items = ItemList.get_all_for_js()
    return render_template("index.html", items=items)


@app.route("/about")
def render_about_html():
    return render_template("about.html")


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")

api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)
