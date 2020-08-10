from sqlalchemy.orm import relationship
import yaml

from .app import db



building_category_table = db.Table(
    'building_category',
    db.Model.metadata,
    db.Column('building_id', db.Integer, db.ForeignKey('building.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Enclave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    buildings = relationship("Building", lazy="dynamic")

    def building(self, id):
        return self.buildings.filter_by(id=id).first()

    def buildings_by_category(self, category):
        return (
            self.buildings
            .join(building_category_table, Category)
            .filter(Category.id==category.id)
        ).all()

    @property
    def categories(self):
        return (
            Category
            .query
            .join(building_category_table)
            .join(Building)
            .filter(Building.enclave_id==self.id)
            .all()
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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)

    __mapper_args__ = {
        "order_by": name,
    }

