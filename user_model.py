from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def create_user(name, raw_password):
    hashed = generate_password_hash(raw_password)
    user = User(username=name, password=hashed)
    db.session.add(user)
    db.session.commit()

def find_user_by_name(name):
    return User.query.filter_by(username=name).first()

def verify_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)