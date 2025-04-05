const express = require("express");
const fs = require("fs");
const path = require("path");
const router = express.Router();

const databasePath = path.join(__dirname, "../database.json");

// Function to read the database
function readDatabase() {
    try {
        if (!fs.existsSync(databasePath)) {
            return { users: [], crops: [] };
        }
        const data = fs.readFileSync(databasePath, "utf8");
        return data ? JSON.parse(data) : { users: [], crops: [] };
    } catch (error) {
        console.error("Error reading database:", error);
        return { users: [], crops: [] };
    }
}

// Function to write to the database
function writeDatabase(data) {
    try {
        fs.writeFileSync(databasePath, JSON.stringify(data, null, 2), "utf8");
    } catch (error) {
        console.error("Error writing to database:", error);
    }
}

// ✅ Route: Add a Crop (for Barter or Resell)
router.post("/add", (req, res) => {
    const { name, type, owner, barterFor, price } = req.body;

    if (!name || !type || !owner) {
        return res.status(400).json({ error: "Crop name, type, and owner are required" });
    }

    let db = readDatabase();

    // Add new crop
    const newCrop = {
        id: db.crops.length + 1,
        name,
        type,  // "Barter" or "Resell"
        owner,
        barterFor: type === "Barter" ? barterFor : null,
        price: type === "Resell" ? price : null
    };

    db.crops.push(newCrop);
    writeDatabase(db);

    res.json({ message: "Crop added successfully", crop: newCrop });
});

// ✅ Route: Get All Crops
router.get("/all", (req, res) => {
    let db = readDatabase();
    res.json(db.crops);
});

// ✅ Route: Search for Barter Crops
router.get("/barter/:cropName", (req, res) => {
    let db = readDatabase();
    const cropName = req.params.cropName.toLowerCase();

    const matchingCrops = db.crops.filter(crop => 
        crop.type === "Barter" && crop.barterFor && crop.barterFor.toLowerCase() === cropName
    );

    if (matchingCrops.length === 0) {
        return res.status(404).json({ message: "No matching barter crops found" });
    }

    res.json(matchingCrops);
});

// ✅ Route: Search for Resell Crops
router.get("/resell/:cropName", (req, res) => {
    let db = readDatabase();
    const cropName = req.params.cropName.toLowerCase();

    const matchingCrops = db.crops.filter(crop => 
        crop.type === "Resell" && crop.name.toLowerCase() === cropName
    );

    if (matchingCrops.length === 0) {
        return res.status(404).json({ message: "No crops available for sale" });
    }

    res.json(matchingCrops);
});

module.exports = router;
