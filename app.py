import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError as e:
        abort(404, message="Store not found.")


@app.post("/store")
def create_store():
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


@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    if "name" not in store_data:
        abort(404, "Bad Request, Ensure name is included in JSON payload")

    try:
        store = stores[store_id]
        store |= store_data
        return store
    except KeyError:
        abort(404, message="Store not found.")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError as e:
        abort(404, message="Item not found.")


@app.post("/item")
def create_item():
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


@app.put("/item/<string:item_id>")
def update_item(item_id):
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


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
