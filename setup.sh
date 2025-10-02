#!/bin/bash
# Conky Trading Dashboard Setup Script
# Run this script to set up the environment after copying files

set -e

CONKY_DIR="$HOME/.config/conky"
VENV_DIR="$HOME/.config/.venv"

echo "🚀 Setting up Conky Trading Dashboard..."

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment and install requirements
echo "📋 Installing Python dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$CONKY_DIR/requirements.txt"

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$CONKY_DIR"/*.py

# Create cache directory if needed
mkdir -p "$CONKY_DIR"

# Test the setup
echo "🧪 Testing setup..."
if "$VENV_DIR/bin/python" "$CONKY_DIR/news_simple.py" count > /dev/null 2>&1; then
    echo "✅ News script working"
else
    echo "⚠️  News script may need internet connection"
fi

if "$VENV_DIR/bin/python" "$CONKY_DIR/sun_moon.py" sunrise > /dev/null 2>&1; then
    echo "✅ Sun/Moon script working"
else
    echo "⚠️  Sun/Moon script may need internet connection"
fi

if "$VENV_DIR/bin/python" "$CONKY_DIR/trading212_api.py" total_value > /dev/null 2>&1; then
    echo "✅ Trading212 script working"
else
    echo "⚠️  Trading212 script needs configuration (trading212_config.json)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Configure Trading212 API key in trading212_config.json"
echo "2. Adjust location settings in config.json if needed"
echo "3. Start conky with: conky -c $CONKY_DIR/conky.conf"
echo ""
echo "📁 All configuration is in: $CONKY_DIR/config.json"