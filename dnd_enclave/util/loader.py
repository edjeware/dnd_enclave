import yaml

from ..app import db
from ..models import Building, Category, Enclave
from .shared import PROJECT_ROOT

def _extract_categories(category_entry):
    if isinstance(category_entry, str):
        return [Category(name=category_entry)]
    return [Category(name=c) for c in category_entry]

def extract_categories(category_entry):
    return [Category.query.filter_by(name=c.name).first() or c for c in _extract_categories(category_entry)]

class EnclaveLoader:
    def __init__(self, source_filepath):
        self.source_filepath = source_filepath
        self._buildings = []
        self._categories = {}

    @property
    def buildings(self):
        if not self._buildings:
            self._load_buildings()
        return self._buildings

    def load(self):
        for entry in yaml.safe_load(open(self.source_filepath))["enclaves"]:
            enclave = Enclave.query.filter_by(name=entry["name"]).first()
            if not enclave:
                enclave = Enclave(name=entry["name"])
            db.session.add(enclave)

            for building_entry in entry["buildings"]:
                building = enclave.building(building_entry["id"])
                if not building:
                    building = Building(**{k:v for k,v in building_entry.items() if k != "category"})
                    enclave.buildings.append(building)
                if "category" in building_entry:
                    categories = extract_categories(building_entry["category"])
                    building.categories.extend(categories)
                    db.session.add_all(categories)
                db.session.add(building)

        db.session.commit()

def load_yaml():
    for item in (PROJECT_ROOT / "data" / "enclaves").glob("*.yaml"):
        EnclaveLoader(item).load()
