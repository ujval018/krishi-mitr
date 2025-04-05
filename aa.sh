#!/bin/bash

echo "🧹 Cleaning up Node.js files (Python-only backend)..."

rm -f krishi-mitr/backend/server.js
rm -f krishi-mitr/backend/models/*.js
rm -f krishi-mitr/backend/routes/*.js
rm -f krishi-mitr/package.json
rm -f krishi-mitr/package-lock.json
rm -rf krishi-mitr/node_modules

echo "✅ Node.js backend cleaned!"
