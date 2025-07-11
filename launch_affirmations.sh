#!/bin/bash
# Backhanded Affirmations Smart Launcher
# Automatically launches GUI or CLI version based on system capabilities

echo "🌟 Backhanded Affirmations 🌟"
echo "================================"
echo "Preparing your daily dose of constructive criticism..."
echo ""

# Function to check if GUI is available
check_gui() {
    # Check for display on Linux/macOS
    if [[ -n "${DISPLAY}" ]] || [[ -n "${WAYLAND_DISPLAY}" ]] || [[ "$(uname)" == "Darwin" ]]; then
        # Try to import tkinter to see if GUI is possible
        if python3 -c "import tkinter" 2>/dev/null; then
            return 0  # GUI available
        fi
    fi
    return 1  # No GUI
}

# Try GUI first
if check_gui; then
    echo "🖥️  GUI detected - launching visual app..."
    echo "Press buttons to get motivated!"
    echo ""
    python3 backhanded_affirmations.py
else
    echo "📟 No GUI detected - launching command-line version..."
    echo "Interactive mode with same snarky content!"
    echo ""
    python3 backhanded_affirmations_cli.py
fi

echo ""
echo "Thanks for using Backhanded Affirmations!"
echo "Remember: You're doing your best, and that's... something! 💫"
