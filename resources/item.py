import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores


blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError as e:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data:
            abort(404, "Bad Request, Ensure price is included in JSON payload")
        if "name" not in item_data:
            abort(404, "Bad Request, Ensure name is included in JSON payload")

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if "price" not in item_data:
            abort(404, "Bad Request, Ensure price is included in JSON payload")
        if "store_id" not in item_data:
            abort(404, "Bad Request, Ensure store_id is included in JSON payload")
        if "name" not in item_data:
            abort(404, "Bad Request, Ensure name is included in JSON payload")

        # check if name and store_id already exists
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        try:
            if item_data["store_id"] not in stores:
                abort(404, message="Store not found.")
        except KeyError:
            abort(404, message="store_id not found.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
