from flask import Blueprint, request, jsonify
import json
import os

crop_bp = Blueprint('crop_bp', __name__)

DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": [], "crops": []}
    with open(DB_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": [], "crops": []}

def save_db(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a Crop for Barter or Resell
@crop_bp.route("/api/crop/add", methods=["POST"])
def add_crop():
    data = request.json
    db = load_db()

    crop = {
        "id": len(db["crops"]) + 1,
        "owner": data["owner"],  
        "name": data["name"],
        "type": data["type"],  # "barter" or "resell"
        "price": data.get("price", None),  # Only for resell
        "exchange_for": data.get("exchange_for", None)  # Only for barter
    }

    db["crops"].append(crop)
    save_db(db)
    return jsonify({"message": "Crop added successfully!", "crop": crop}), 201

# Get Available Crops for Barter or Resell
@crop_bp.route("/api/crop/list", methods=["GET"])
def list_crops():
    db = load_db()
    return jsonify({"crops": db["crops"]}), 200
