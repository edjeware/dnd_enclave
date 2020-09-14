from ..app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)

    __mapper_args__ = {
        "order_by": name,
    }

