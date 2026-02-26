#!/bin/bash

# Build script for Frappe Cloud deployment
echo "🚀 Building Ascra Frontend for Frappe Cloud..."

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found in frontend directory!"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
if command -v yarn &> /dev/null; then
    yarn install --frozen-lockfile
else
    npm install
fi

# Build the application
echo "🔨 Building frontend application..."
if command -v yarn &> /dev/null; then
    yarn build
else
    npm run build
fi

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully!"
    echo "📁 Built files are in: ascra_frontend/public/frontend/"
    
    # List the built files
    echo "📋 Build output:"
    ls -la ../ascra_frontend/public/frontend/
    
    echo "🎯 Frappe Cloud deployment ready!"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
