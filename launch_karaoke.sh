#!/bin/bash
# Keyboard Karaoke Game Launcher
# This script automatically sets up the required dependencies and launches the game

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

# Install/upgrade pygame if needed
echo "Checking dependencies..."
pip install pygame > /dev/null 2>&1

echo "🚀 Launching mission..."
echo "Press SPACE in the game window to start your spy mission!"
echo ""

# Launch the game
python keyboard_karaoke.py
