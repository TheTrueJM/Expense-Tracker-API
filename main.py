from config import app, db
from models import User, Tasks

from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta, UTC
import jwt, hashlib, os



def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "jwt-token" not in request.headers:
            return jsonify({"message": "JSON Web Token Missing"}), 401
        
        try:
            token = request.headers["jwt-token"]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            current_user = User.query.filter_by(username=data["username"]).first()
            if not current_user:
                raise ValueError
        except:
            return jsonify({"message": "Invalid JSON Web Token"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated



@app.route("/")
@authentication_required
def home(user):
    return jsonify({})



def password_hasher(password, salt):
    hashed_password = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1, dklen=32)
    final_password = salt[:16] + hashed_password + salt[-16:]
    return final_password

@app.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")

    feedback = ""
    if not username:
        feedback = "Username is required"
    elif User.query.filter_by(username=username).first():
        feedback = "Username is already taken"
    elif not password:
        feedback = "Password is required"

    if feedback:
        return jsonify({"message": feedback}), 401
    
    hashed_password = password_hasher(password.encode('utf-8'), os.urandom(32))
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Successful new user sign up"})

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    feedback = ""
    if not username or not password:
        feedback = f"{"Username" if password else "Password"} is required"
    else:
        user = User.query.filter_by(username=username).first()
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



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)