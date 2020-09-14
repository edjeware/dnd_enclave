from sqlalchemy.orm import relationship

from ..app import db
from .building import Building, building_category_table
from .category import Category

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
