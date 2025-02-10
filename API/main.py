from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

#MongoDB configuration
# ✅ MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)


# ✅ Drinks Collection in MongoDB
drinks_collection = mongo.db.drinks

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/drinks') #get all drinks
def get_all_drinks():
    #we need to fist add all the drinks into the list
    drinks = list(drinks.collection.find({}, {"_id": 0})) # Convert cursor to list and exclude _id 
    return jsonify({"drinks": drinks})


# ✅ Get a single drink by ID
@app.route('/drinks/<id>', methods=['GET'])
def get_drink(drink_id):
    try:
        drink = drinks_collection.find_one({"_id": ObjectId(drink_id)}, {"_id": 0})
        if drink:
            return jsonify({"drink": drink})
        return jsonify({"error": "Drink not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400
        

# ✅ Add a new drink
@app.route('/add_drink', methods=['POST'])
def add_drink():
    data.request.json()
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
