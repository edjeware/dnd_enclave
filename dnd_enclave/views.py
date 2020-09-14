from flask import render_template

from .app import app
from .models import Building, Category, Enclave


@app.route('/')
def enclave_index():
    return render_template(
        "enclave_index.html",
        enclaves=Enclave.query.all(),
    )

@app.route('/enclaves/<int:enclave_id>')
def enclave_show(enclave_id):
    enclave = Enclave.query.get(enclave_id)
    return render_template(
        "enclave_show.html",
        buildings=enclave.buildings,
        enclave=enclave,
    )

@app.route('/enclaves/<int:enclave_id>/category/<string:category>')
def enclave_category(enclave_id, category):
    enclave = Enclave.query.get(enclave_id)
    category = Category.query.filter_by(name=category).first()
    return render_template(
        "enclave_show.html",
        buildings=enclave.buildings_by_category(category),
        category=category,
        enclave=enclave,
    )

@app.route('/enclaves/<int:enclave_id>/buildings/<int:building_id>')
def building_show(enclave_id, building_id):
    building = Building.by_ids(enclave_id=enclave_id, building_id=building_id).first()
    return render_template(
        "building_show.html",
        building=building,
        enclave=Enclave.query.get(enclave_id),
    )
