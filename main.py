from flask import Flask, request, jsonify
from flask_cors import CORS
from user_model import db, create_user, find_user_by_name, verify_password
from config import SECRET_KEY
import jwt
import datetime

# Ініціалізація додатку
app = Flask(__name__)
CORS(app)

# Конфігурація
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

# Підключення БД
db.init_app(app)

# Створення таблиць при запуску
with app.app_context():
    db.create_all()

# Реєстрація
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": False, "message": "Порожні поля"}), 400

    if find_user_by_name(username):
        return jsonify({"status": False, "message": "Користувач вже є"}), 409

    create_user(username, password)
    return jsonify({"status": True, "message": "Успішно зареєстровано"}), 201

# Вхід
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = find_user_by_name(username)
    if not user or not verify_password(user.password, password):
        return jsonify({"status": False, "message": "Невірні дані"}), 401

    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"status": True, "token": token})