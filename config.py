from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "ExampleKey-ChangeLater" # Fix This | os.environ.get('SECRET_KEY') or 'this is a secret'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expensetracker.db"

db = SQLAlchemy(app)