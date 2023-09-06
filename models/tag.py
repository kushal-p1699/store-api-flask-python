from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.String, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    # query will go into secondary table and fetch the item id which is mapped with a this tag and returns the items
    # example of many-to-many mapping
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
