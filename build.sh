#!/bin/bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Upgrade pip and setuptools
echo "📦 Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install numpy first (required for scikit-learn)
echo "📦 Installing numpy..."
pip install numpy==1.24.3

# Install scikit-learn with specific flags
echo "📦 Installing scikit-learn..."
pip install scikit-learn==1.3.0 --no-build-isolation

# Install remaining dependencies
echo "📦 Installing remaining dependencies..."
pip install -r requirements.txt

echo "✅ Build completed successfully!" 