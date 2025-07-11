#!/bin/bash
# Smart Keyboard Karaoke Launcher
# Tries full version first, falls back to lightweight version if dependencies are missing

echo "🕵️‍♂️  Keyboard Karaoke: Spy Theme Edition 🕵️‍♂️"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install pygame (required for both versions)
echo "Installing basic dependencies..."
pip install pygame > /dev/null 2>&1

# Try to install numpy for full version
echo "Checking for advanced audio support..."
if pip install numpy > /dev/null 2>&1; then
    NUMPY_AVAILABLE=true
    echo "✅ NumPy available - using full version with rich audio"
else
    NUMPY_AVAILABLE=false
    echo "⚠️  NumPy not available - using lightweight version"
fi

echo ""
echo "🚀 Launching mission..."

# Try full version first if numpy is available
if [ "$NUMPY_AVAILABLE" = true ]; then
    echo "Starting full version with rich audio synthesis..."
    echo "Press SPACE in the game window to start your spy mission!"
    echo ""
    python keyboard_karaoke.py
else
    echo "Starting lightweight version with simplified audio..."
    echo "Press SPACE in the game window to start your spy mission!"
    echo ""
    python keyboard_karaoke_light.py
fi
