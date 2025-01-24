from config import app, db
from models import Users, Tasks
from category import Category

from flask import request, jsonify
from flask_restful import reqparse, inputs
from functools import wraps
from datetime import datetime, timedelta, UTC
import jwt, hashlib, os



user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True, help="Username is required")
user_args.add_argument("password", type=str, required=True, help="Password is required")

expense_args = reqparse.RequestParser()
expense_args.add_argument("description", type=str, required=True, help="Expense description is required")
expense_args.add_argument("category", type=str, choices=Category.names(), required=True, help="Valid expense category is required")
expense_args.add_argument("amount", type=float, required=True, help="Expense cost amount is required")

time_filters = reqparse.RequestParser()
time_filters.add_argument("time-period", type=str, choices={"week", "month", "three-months"}, location="args", help="Valid time peroids are week, month, and three-months")
time_filters.add_argument("time-start", type=inputs.date, location="args", help="Valid time start must be a date")
time_filters.add_argument("time-end", type=inputs.date, location="args", help="Valid time end must be a date")



def password_hasher(password, salt):
    hashed_password = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1, dklen=32)
    final_password = salt[:16] + hashed_password + salt[-16:]
    return final_password


@app.route("/signup", methods=["POST"])
def signup():
    args = user_args.parse_args()
    username, password = args["username"], args["password"]

    if Users.query.filter_by(username=username).first():
        return jsonify({"message": "Username is already taken"}), 401
    
    hashed_password = password_hasher(password.encode('utf-8'), os.urandom(32))
    user = Users(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Successful new user sign up"}), 201

@app.route("/login", methods=["POST"])
def login():
    args = user_args.parse_args()
    username, password = args["username"], args["password"]

    feedback = ""
    user = Users.query.filter_by(username=username).first()
    if not user:
        feedback = f"User '{username}' was not found"
    else:
        password_salt = user.password[:16] + user.password[-16:]
        hashed_password = password_hasher(password.encode('utf-8'), password_salt)
        if hashed_password != user.password:
            feedback = "Password is incorrect"
    
    if feedback:
        return jsonify({"message": feedback}), 401
    
    token = jwt.encode(
        {"username": user.username, "exp": datetime.now(UTC) + timedelta(minutes=30)},
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"message": "Successful user login", "jwt-token": token})



def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "jwt-token" not in request.headers:
            return jsonify({"message": "JSON Web Token Missing"}), 401
        
        try:
            token = request.headers["jwt-token"]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            current_user = Users.query.filter_by(username=data["username"]).first()
            if not current_user:
                raise ValueError
        except:
            return jsonify({"message": "Invalid JSON Web Token"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/expenses")
@authentication_required
def expenses(user):
    args = time_filters.parse_args()

    if args["time-period"]:
        chosen_date = datetime.now(UTC).date()
        match args["time-period"]:
            case "week":
                chosen_date -= timedelta(days=7)
            case "month":
                chosen_date -= timedelta(days=30)
            case "three-months":
                chosen_date -= timedelta(days=90)
        user_expenses = Tasks.query.filter(Tasks.username==user.username, chosen_date <= Tasks.date).all()
    
    elif args["time-start"] or args["time-end"]:
        if not args["time-end"]:
            user_expenses = Tasks.query.filter(Tasks.username==user.username, args["time-start"] <= Tasks.date).all()
        elif not args["time-start"]:
            user_expenses = Tasks.query.filter(Tasks.username==user.username, Tasks.date <= args["time-end"]).all()
        else:
            user_expenses = Tasks.query.filter(Tasks.username==user.username, args["time-start"] <= Tasks.date, Tasks.date <= args["time-end"]).all()
    
    else:
        user_expenses = Tasks.query.filter_by(username=user.username).all()
    
    return jsonify({"expenses": [expense.serialize() for expense in user_expenses]})

@app.route("/expenses", methods=["POST"])
@authentication_required
def create_expense(user):
    args = expense_args.parse_args()
    description, category, amount = args["description"], args["category"], args["amount"]

    if amount <= 0:
        return jsonify({"message": "Invalid cost amount"}), 400

    expense = Tasks(username=user.username, description=description, category=category, amount=amount)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"expense": expense.serialize()}), 201


@app.route("/expenses/<int:id>")
@authentication_required
def expense(user, id):
    user_expense = Tasks.query.filter_by(username=user.username, id=id).first()
    if not user_expense:
        return jsonify({"message": "No expense found"}), 404
    return jsonify({"expense": user_expense.serialize()})

@app.route("/expenses/<int:id>", methods=["PUT"])
@authentication_required
def update_expense(user, id):
    user_expense = Tasks.query.filter_by(username=user.username, id=id).first()
    if not user_expense:
        return jsonify({"message": "No expense found"}), 404
    
    args = expense_args.parse_args()
    if args["amount"] <= 0:
        return jsonify({"message": "Invalid cost amount"}), 400

    user_expense.description = args["description"]
    user_expense.category = args["category"]
    user_expense.amount = args["amount"]
    db.session.commit()
    return jsonify({"expense": user_expense.serialize()})

@app.route("/expenses/<int:id>", methods=["DELETE"])
@authentication_required
def delete_expense(user, id):
    user_expense = Tasks.query.filter_by(username=user.username, id=id).first()
    if not user_expense:
        return jsonify({"message": "No expense found"}), 404
    
    db.session.delete(user_expense)
    db.session.commit()
    return jsonify({}), 204



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
