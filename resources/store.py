import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

# Blurprint divides an api into multiple segments like store, items etc.

blp = Blueprint("Stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError as e:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

    def put(self, store_id):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(404, "Bad Request, Ensure name is included in JSON payload")

        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(404, "Bad Request, Ensure name is included in JSON payload")

        # check if name already exists
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404, message="Store already exists.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = store_data
        return new_store, 201
