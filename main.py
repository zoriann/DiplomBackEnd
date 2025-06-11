from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')  # ВАЖЛИВО: саме такий шлях
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/products")
def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route("/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    print("Нове замовлення:", data)
    return jsonify({"success": True})