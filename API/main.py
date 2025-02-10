from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import config 
from bson.objectid import ObjectId

app = Flask(__name__)

mongo = PyMongo(app, uri=config.MONGO_URI)

# ✅ Ensure db is initialized correctly
if mongo.db is None:
    raise RuntimeError("MongoDB connection failed!")

# ✅ Define collection correctly AFTER initializing mongo
drinks_collection = mongo.db["drinks"]  # Access collection safely


@app.route('/')
def index():
    return "Hello, World!"

# ✅ Get all drinks
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    drinks = list(drinks_collection.find({}, {"_id": 0}))  # Convert cursor to list and exclude _id
    return jsonify({"drinks": drinks})


# ✅ Get a single drink by ID
@app.route('/drinks/<id>', methods=['GET'])
def get_drink(id):
    try:
        drink = drinks_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
        if drink:
            return jsonify({"drink": drink})
        return jsonify({"error": "Drink not found"}), 404
    except Exception:
        return jsonify({"error": "Invalid ID format"}), 400


# ✅ Add a new drink
@app.route('/add_drink', methods=['POST'])
def add_drink():
    data = request.get_json()
    if "name" not in data or "description" not in data:
        return jsonify({"error": "Name and description are required"}), 400
    
    new_drink = {
        "name": data["name"],
        "description": data["description"]
    }
    drink_id = drinks_collection.insert_one(new_drink).inserted_id
    return jsonify({"message": "Drink added!", "id": str(drink_id)})


# ✅ Delete all drinks
@app.route('/delete_all_drinks', methods=['DELETE'])
def delete_all_drinks():
    drinks_collection.delete_many({})
    return jsonify({"message": "All drinks deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
