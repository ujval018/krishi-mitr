@echo off
echo 🚀 Starting Krishi Mitr Full Setup...

:: Step 1: Python Virtual Environment
echo 📦 Creating Python virtual environment (if not exists)...
python -m venv backend\venv

echo 🐍 Activating Python environment and installing requirements...
call backend\venv\Scripts\activate
pip install -r backend\requirements.txt

:: Step 2: Node.js Dependencies
echo 📦 Installing Node.js dependencies...
cd krishi-mitr
npm install
cd ..

:: Step 3: Backend Check
set USE_PYTHON_BACKEND=false
set USE_NODE_BACKEND=false

if exist krishi-mitr\backend\app.py (
    set USE_PYTHON_BACKEND=true
)

if exist krishi-mitr\backend\server.js (
    set USE_NODE_BACKEND=true
)

if "%USE_PYTHON_BACKEND%"=="true" (
    echo 🚀 Launching Python backend...
    cd krishi-mitr\backend
    python app.py
) else if "%USE_NODE_BACKEND%"=="true" (
    echo 🚀 Launching Node.js backend...
    cd krishi-mitr\backend
    node server.js
) else (
    echo ❌ No valid backend found. Please check the 'backend' folder.
)
