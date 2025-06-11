from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/order", methods=["POST"])
def receive_order():
    data = request.get_json()
    print("Нове замовлення:")
    print(data)  # Виводить у лог на Railway
    return jsonify({"success": True, "message": "Замовлення отримано!"})

if __name__ == "__main__":
    app.run()