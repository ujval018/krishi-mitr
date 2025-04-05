const express = require("express");
const fs = require("fs");
const path = require("path");
const router = express.Router();

const databasePath = path.join(__dirname, "../database.json");

// Function to read the database
function readDatabase() {
    try {
        if (!fs.existsSync(databasePath)) {
            return { users: [], crops: [] }; // ✅ Handle missing file
        }
        const data = fs.readFileSync(databasePath, "utf8");
        return data ? JSON.parse(data) : { users: [], crops: [] }; // ✅ Handle empty file
    } catch (error) {
        console.error("Error reading database:", error);
        return { users: [], crops: [] }; // ✅ Safe fallback
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

// ✅ Route: User Registration
router.post("/register", (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({ error: "Username and password required" });
    }

    let db = readDatabase();

    // Check if user already exists
    if (db.users.find(user => user.username === username)) {
        return res.status(400).json({ error: "User already exists" });
    }

    // Save new user
    db.users.push({ username, password });
    writeDatabase(db);

    res.json({ message: "User registered successfully" });
});

// ✅ Route: User Login
router.post("/login", (req, res) => {
    const { username, password } = req.body;
    let db = readDatabase();

    const user = db.users.find(user => user.username === username && user.password === password);
    if (!user) {
        return res.status(401).json({ error: "Invalid username or password" });
    }

    res.json({ message: "Login successful" });
});

module.exports = router;
