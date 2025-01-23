from config import db
from category import Category

from datetime import datetime, UTC

class Users(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary(64))

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey("users.username"))
    description = db.Column(db.String)
    category = db.Column(db.Enum(Category))
    amount = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.now(UTC).date)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "description": self.description,
            "category": self.category.name,
            "amount": self.amount,
            "date": self.date
        }
    