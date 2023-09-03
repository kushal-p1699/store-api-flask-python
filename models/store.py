from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # keeping assosiated items object
    # setting lazy=dymanic will prevent querying items everytime when store model is called. The request sent to query items only when we tell it. hence, It reduces time taken to query stores
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
