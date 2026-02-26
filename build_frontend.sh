#!/bin/bash

# Build script for Ascra Frontend - Production Deployment
# Similar to HRMS deployment pattern

echo "🚀 Building Ascra Frontend for Production..."

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    yarn install
fi

# Build the frontend application
echo "🔨 Building frontend application..."
yarn build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully!"
    echo "📁 Built files are in: ascra_frontend/public/frontend/"
    echo "🌐 HTML template is in: ascra_frontend/www/frontend.html"
    echo ""
    echo "🎯 Production Deployment Ready!"
    echo "   - Frontend assets: /assets/ascra_frontend/frontend/"
    echo "   - Access URL: http://your-site.com/frontend"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Deploy the Frappe app: bench --site your-site install-app ascra_frontend"
    echo "   2. Access frontend at: http://your-site.com/frontend"
    echo "   3. Frontend will be served as static assets from the app"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
