from ..app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enclave_id = db.Column(db.Integer, db.ForeignKey('enclave.id'))
