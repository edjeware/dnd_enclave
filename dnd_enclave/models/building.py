from sqlalchemy.orm import relationship

from ..app import db

building_category_table = db.Table(
    'building_category',
    db.Model.metadata,
    db.Column('building_id', db.Integer, db.ForeignKey('building.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enclave_id = db.Column(db.Integer, db.ForeignKey('enclave.id'))
    name = db.Column(db.String(256), nullable=False)
    is_guild = db.Column(db.Boolean, default=False)

    categories = relationship(
        "Category",
        lazy="dynamic",
        secondary=building_category_table,
    )
