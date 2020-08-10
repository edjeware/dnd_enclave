from pathlib import Path
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

build_path = Path("build")
build_path.mkdir(exist_ok=True)
build_path /= "app.db"
default_path = build_path.absolute().as_uri().replace("file:/","sqlite://")
print(f"Build path: {default_path}")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI", default_path,
)

if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
