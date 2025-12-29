#!/bin/bash

# Build script for Render deployment

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Train the ML model
echo "🤖 Training ML model..."
python scripts/train_model.py

echo "✅ Build complete!"
