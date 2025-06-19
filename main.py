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

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO products (name, price, category, image) VALUES (?, ?, ?, ?)",
        (data["name"], data["price"], data["category"], data["image"]),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Товар додано!"})

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Товар видалено!"})

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "UPDATE products SET name = ?, price = ?, category = ?, image = ? WHERE id = ?",
        (data["name"], data["price"], data["category"], data["image"], product_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Товар оновлено!"})

@app.route("/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    print("Замовлення отримано:", data)
    return jsonify({"success": True, "message": "Замовлення збережено!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)