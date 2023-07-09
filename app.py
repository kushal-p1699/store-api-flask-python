from flask import Flask, request

app = Flask(__name__)


stores = [
    {
        "name": "My Store",
        "items": [
            {"name": "laptop", "price": 1123},
            {"name": "printer", "price": 99.00},
        ],
    }
]


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_new_store():
    request_json = request.get_json()
    new_store = {"name": request_json["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_new_item(name):
    request_json = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_json["name"], "price": request_json["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "No store found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return {"store": store}
    return {"message": "No store found"}, 404


@app.get("/store/<string:name>/items")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "No store found"}, 404
