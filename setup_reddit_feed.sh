#!/bin/bash
# Quick setup script for Reddit News Feed

echo "🚀 Reddit News Feed - Quick Setup"
echo "=================================="
echo ""

echo "This will help you get started with your personalized Reddit feed."
echo ""

# Check if config exists
if [ -f "feed_config.json" ]; then
    echo "📋 Configuration file already exists."
    echo "Current subreddits will be shown during setup."
else
    echo "📝 Creating new configuration..."
fi

echo ""
echo "🛠️  Starting interactive setup..."
echo ""

# Run the setup command
uv run python main.py setup

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 What's next?"
echo "1. Test your feed:     ./launch.sh"
echo "2. Preview subreddit:  uv run python main.py preview <subreddit>"
echo "3. View config:        uv run python main.py config"
echo "4. See demo:           uv run python demo.py"
echo ""
echo "📰 Happy browsing!"
