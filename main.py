from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/products")
def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route("/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    print("Замовлення отримано:", data)
    return jsonify({"success": True, "message": "Замовлення збережено!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)