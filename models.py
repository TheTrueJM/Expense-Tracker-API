from config import db
from datetime import datetime

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    # tasks = db.relationship("Tasks")

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey("user.username"), primary_key=True)
    description = db.Column(db.String)
    category = db.Column(db.String)
    ammount = db.Column(db.Float)
    date = db.Column(db.Date)