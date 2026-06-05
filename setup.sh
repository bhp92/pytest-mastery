#!/bin/bash
# setup.sh — Run once after cloning to set up everything
# Usage: bash setup.sh

set -e

echo "🧪 Pytest Mastery — Setup"
echo "========================="

# Check Python version
python3 --version || { echo "❌ Python 3 not found. Install Python 3.9+"; exit 1; }

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate     # activate the venv"
echo "  pytest week1/ -v              # run Week 1 tests"
echo "  python3 -m http.server 8080   # serve the dashboard"
echo "  # then open http://localhost:8080 in your browser"
echo ""
echo "Happy studying! 🚀"
