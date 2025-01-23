from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from os import environ

app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("FLASK_KEY", "default-placeholder")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expensetracker.db"

db = SQLAlchemy(app)