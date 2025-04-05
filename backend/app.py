"""
Krishi Mitr Backend API

A Flask-based backend for Krishi Mitr farming application that provides:
- User authentication (register/login)
- Crop management (add/list/barter/buy crops)
- Simple JSON-based database storage

API Endpoints:
- /api/auth/register (POST) - User registration
- /api/auth/login (POST) - User login
- /api/crop/add (POST) - Add new crop
- /api/crop/list (GET) - List available crops
- /api/crop/barter/<crop_id> (POST) - Barter a crop
- /api/crop/buy/<crop_id> (POST) - Buy a crop

Database Schema:
{
    "users": [
        {"username": str, "password": str}
    ],
    "crops": [
        {
            "id": str (UUID),
            "owner": str,
            "name": str,
            "type": str ("barter"|"resell"),
            "price": float (optional),
            "exchange_for": str (optional)
        }
    ]
}
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route("/")
def home():
    """Root endpoint that returns API status
    
    Returns:
        str: Simple message indicating API is running
    """
    return "🌿 Krishi Mitr API is running!"

# Database configuration
DB_FILE = "database.json"

def load_db():
    """Load the JSON database file
    
    Returns:
        dict: Database contents or empty structure if file doesn't exist/corrupt
    """
    if not os.path.exists(DB_FILE):
        return {"users": [], "crops": []}
    with open(DB_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": [], "crops": []}

def save_db(data):
    """Save data to the JSON database file
    
    Args:
        data (dict): Database contents to save
    """
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ---------------------- AUTH ROUTES ----------------------

@app.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new user
    
    Request Body:
        {
            "username": str (min 4 chars),
            "password": str (min 6 chars)
        }
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": "User registered successfully"}, 201
            Error: {"message": error message}, 400/401
            
    Example:
        POST /api/auth/register
        {
            "username": "farmer1",
            "password": "secure123"
        }
    """
    data = request.json
    
    # Input validation
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400
    if len(data["username"]) < 4:
        return jsonify({"message": "Username must be at least 4 characters"}), 400
    if len(data["password"]) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    db = load_db()

    # Check if user already exists
    for user in db["users"]:
        if user["username"] == data["username"]:
            return jsonify({"message": "User already exists"}), 400

    # Add new user
    db["users"].append({
        "username": data["username"].strip(),
        "password": data["password"]  # In production, should hash password
    })
    save_db(db)
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    """Authenticate an existing user
    
    Request Body:
        {
            "username": str,
            "password": str
        }
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": "Login successful", "username": str}, 200
            Error: {"message": "Invalid credentials"}, 401
            
    Example:
        POST /api/auth/login
        {
            "username": "farmer1",
            "password": "secure123"
        }
    """
    data = request.json
    
    # Input validation
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password are required"}), 400

    db = load_db()

    for user in db["users"]:
        if user["username"] == data["username"] and user["password"] == data["password"]:
            return jsonify({
                "message": "Login successful",
                "username": user["username"]
            }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

import uuid  # Import for unique crop IDs

# ---------------------- CROP BARTER & RESELL ROUTES ----------------------

@app.route("/api/crop/add", methods=["POST"])
def add_crop():
    """Add a new crop for barter or resale
    
    Request Body:
        {
            "owner": str (username),
            "name": str (crop name),
            "type": str ("barter"|"resell"),
            "price": float (required if type="resell"),
            "exchange_for": str (required if type="barter")
        }
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": str, "crop": crop_data}, 201
            Error: {"message": error message}, 400
            
    Example:
        POST /api/crop/add
        {
            "owner": "farmer1",
            "name": "Wheat",
            "type": "barter",
            "exchange_for": "Rice"
        }
    """
    data = request.json
    
    # Input validation
    required_fields = ["owner", "name", "type"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": f"Required fields: {', '.join(required_fields)}"}), 400
    
    if data["type"] not in ["barter", "resell"]:
        return jsonify({"message": "Type must be 'barter' or 'resell'"}), 400
        
    if data["type"] == "resell" and "price" not in data:
        return jsonify({"message": "Price is required for resell"}), 400
    if data["type"] == "barter" and "exchange_for" not in data:
        return jsonify({"message": "Exchange_for is required for barter"}), 400

    db = load_db()

    crop = {
        "id": str(uuid.uuid4()),
        "owner": data["owner"].strip(),
        "name": data["name"].strip(),
        "type": data["type"],
        "price": data.get("price", 0) if data["type"] == "resell" else None,
        "exchange_for": data.get("exchange_for", "").strip() if data["type"] == "barter" else None
    }

    db["crops"].append(crop)
    save_db(db)
    return jsonify({"message": "Crop added successfully!", "crop": crop}), 201

@app.route("/api/crop/list", methods=["GET"])
def list_crops():
    """List all available crops
    
    Returns:
        tuple: (list of crops, status code)
            Success: [crop1, crop2, ...], 200
            
    Example:
        GET /api/crop/list
        Returns:
        [
            {
                "id": "uuid",
                "owner": "farmer1",
                "name": "Wheat",
                "type": "barter",
                "exchange_for": "Rice"
            },
            ...
        ]
    """
    db = load_db()
    return jsonify(db["crops"]), 200

@app.route("/api/crop/barter/<crop_id>", methods=["POST"])
def barter_crop(crop_id):
    """Complete a crop barter transaction
    
    Args:
        crop_id (str): UUID of crop to barter
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": str, "crop": crop_data}, 200
            Error: {"message": error message}, 400/404
            
    Example:
        POST /api/crop/barter/123e4567-e89b-12d3-a456-426614174000
    """
    # Validate crop_id format
    if not crop_id or len(crop_id) != 36:  # UUID length
        return jsonify({"message": "Invalid crop ID format"}), 400

    db = load_db()

    for crop in db["crops"]:
        if crop["id"] == crop_id:
            if crop["type"] != "barter":
                return jsonify({"message": "Crop is not available for barter"}), 400
            db["crops"].remove(crop)
            save_db(db)
            return jsonify({
                "message": "Crop bartered successfully!",
                "crop": crop
            }), 200

    return jsonify({"message": "Crop not found"}), 404

@app.route("/api/crop/buy/<crop_id>", methods=["POST"])
def buy_crop(crop_id):
    """Complete a crop purchase transaction
    
    Args:
        crop_id (str): UUID of crop to buy
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": str, "crop": crop_data}, 200
            Error: {"message": error message}, 400/404
            
    Example:
        POST /api/crop/buy/123e4567-e89b-12d3-a456-426614174000
    """
    # Validate crop_id format
    if not crop_id or len(crop_id) != 36:  # UUID length
        return jsonify({"message": "Invalid crop ID format"}), 400

    db = load_db()

    for crop in db["crops"]:
        if crop["id"] == crop_id:
            if crop["type"] != "resell":
                return jsonify({"message": "Crop is not available for purchase"}), 400
            db["crops"].remove(crop)
            save_db(db)
            return jsonify({
                "message": "Crop purchased successfully!",
                "crop": crop
            }), 200

    return jsonify({"message": "Crop not found"}), 404

# ---------------------- PRICING API ROUTES ----------------------

@app.route("/api/pricing", methods=["GET"])
def get_all_prices():
    """Get all crop prices
    
    Returns:
        tuple: (list of prices, status code)
            Success: [price1, price2, ...], 200
            
    Example:
        GET /api/pricing
        Returns:
        [
            {
                "crop": "Wheat",
                "category": "Cereals",
                "msp": 2275,
                "market_price": 2400,
                "last_updated": "2023-11-15"
            },
            ...
        ]
    """
    db = load_db()
    if "prices" not in db:
        return jsonify([]), 200
    return jsonify(db["prices"]), 200

@app.route("/api/pricing/<crop_name>", methods=["GET"])
def get_crop_price(crop_name):
    """Get price for specific crop
    
    Args:
        crop_name (str): Name of crop to get price for
    
    Returns:
        tuple: (price data, status code)
            Success: price_data, 200
            Error: {"message": "Price not found"}, 404
            
    Example:
        GET /api/pricing/Wheat
    """
    db = load_db()
    if "prices" not in db:
        return jsonify({"message": "Price not found"}), 404
        
    for price in db["prices"]:
        if price["crop"].lower() == crop_name.lower():
            return jsonify(price), 200
    return jsonify({"message": "Price not found"}), 404

@app.route("/api/pricing", methods=["POST"])
def update_prices():
    """Update price data (admin only)
    
    Request Body:
        {
            "prices": [
                {
                    "crop": str,
                    "category": str,
                    "msp": float,
                    "market_price": float
                },
                ...
            ]
        }
    
    Returns:
        tuple: (response JSON, status code)
            Success: {"message": "Prices updated"}, 200
            Error: {"message": error message}, 400
            
    Example:
        POST /api/pricing
        {
            "prices": [
                {
                    "crop": "Wheat",
                    "category": "Cereals",
                    "msp": 2300,
                    "market_price": 2450
                }
            ]
        }
    """
    data = request.json
    if not data or "prices" not in data:
        return jsonify({"message": "Prices data required"}), 400
        
    db = load_db()
    db["prices"] = data["prices"]
    save_db(db)
    return jsonify({"message": "Prices updated successfully"}), 200
# ---------------------- RUN SERVER ----------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

