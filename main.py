from flask import Flask, request, jsonify
from flask_cors import CORS
from user_model import db, create_user, find_user_by_name, verify_password
from config import SECRET_KEY
import jwt, datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

db.init_app(app)

@app.before_first_request
def initialize():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    info = request.get_json()
    username, password = info.get("username"), info.get("password")

    if find_user_by_name(username):
        return jsonify({"status": False, "message": "Користувач вже існує"}), 409

    create_user(username, password)
    return jsonify({"status": True, "message": "Користувач створений"})

@app.route("/login", methods=["POST"])
def login():
    info = request.get_json()
    username, password = info.get("username"), info.get("password")

    user = find_user_by_name(username)
    if not user or not verify_password(user.password, password):
        return jsonify({"status": False, "message": "Дані невірні"}), 401

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"status": True, "token": token})