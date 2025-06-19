from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route("/api/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "Файл не знайдено"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "Порожнє ім’я файлу"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"success": True, "message": "Файл збережено", "filename": filename}), 200
    return jsonify({"success": False, "message": "Недозволений формат"}), 400

@app.route("/static/images/<filename>")
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    print("Замовлення отримано:", data)
    return jsonify({"success": True, "message": "Замовлення збережено!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
