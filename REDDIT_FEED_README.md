# 🗞️ Reddit News Feed

A personalized news aggregator that creates a custom feed from your favorite Reddit communities.

## ✨ Features

- **Personalized Feed**: Aggregate content from multiple subreddits
- **Smart Filtering**: Filter by score, keywords, and time
- **Interactive Browsing**: Navigate through posts with a clean interface
- **Configuration Management**: Customize your preferences
- **Real-time Updates**: Refresh your feed on demand
- **Post Details**: View full post information and open in browser

## 🚀 Quick Start

```bash
# Launch the news feed
./launch.sh

# Or run directly
uv run python main.py feed

# Interactive setup
uv run python main.py setup

# Show configuration
uv run python main.py config
```

## 📋 Commands

### Main Feed
```bash
# Show your personalized feed
uv run python main.py feed

# Run setup first time
uv run python main.py feed --setup

# Show current config
uv run python main.py feed --config
```

### Configuration
```bash
# Interactive setup
uv run python main.py setup

# View current settings
uv run python main.py config
```

### Preview
```bash
# Preview a specific subreddit
uv run python main.py preview programming --limit 5
uv run python main.py preview worldnews --limit 10
```

## ⚙️ Configuration Options

The app creates a `feed_config.json` file with your preferences:

- **Subreddits**: List of communities to follow
- **Sort Order**: hot, new, top, or rising
- **Time Filter**: hour, day, week, month, year, all
- **Post Limits**: Maximum posts per subreddit and total
- **Filtering**: Minimum score, keyword exclusions
- **Topics**: Your areas of interest

### Example Configuration
```json
{
  "subreddits": [
    "programming", "MachineLearning", "technology", 
    "worldnews", "science", "Python", "datascience"
  ],
  "sort_by": "hot",
  "time_filter": "day",
  "max_posts_per_sub": 5,
  "max_total_posts": 25,
  "minimum_score": 10,
  "exclude_keywords": ["spoiler", "NSFW"]
}
```

## 🎯 Default Subreddits

The app comes with curated defaults:
- **Tech**: programming, technology, Python, datascience
- **Science**: science, MachineLearning, artificial intelligence  
- **News**: worldnews, news
- **Security**: cybersecurity

## 🖥️ Interactive Features

### Feed Browsing
- **Ranked Display**: Posts ranked by score and engagement
- **Quick Info**: Score, comments, author, post age
- **Subreddit Tags**: See which community each post comes from

### Post Details
- **Full Information**: Complete title, content preview, links
- **Browser Integration**: Open URLs or Reddit comments
- **Navigation**: Easy back-and-forth between list and details

### Live Updates
- **Refresh Command**: Get latest posts without restarting
- **Real-time Timestamps**: See how fresh your content is
- **Status Indicators**: Visual feedback during fetching

## 📊 Content Filtering

### Automatic Filtering
- **Score Threshold**: Hide low-quality posts
- **Keyword Exclusion**: Filter out unwanted content
- **Duplicate Removal**: No repeated posts from different subs
- **Quality Control**: Focus on engaging content

### Smart Ranking
- **Score-based**: Higher scored posts appear first
- **Recency Factor**: Balance popular and fresh content
- **Engagement Metrics**: Comments and discussion weight

## 🛠️ Technical Features

- **Fast Performance**: Efficient Reddit API usage
- **Rate Limiting**: Respectful server interaction
- **Error Handling**: Graceful failure recovery
- **Caching**: Reduce unnecessary API calls
- **Cross-platform**: Works on macOS, Linux, Windows

## 📱 Usage Examples

### Daily News Routine
```bash
# Morning briefing
uv run python main.py feed

# Browse a few posts, then refresh
# Use 'r' command in interactive mode
```

### Topic Research
```bash
# Preview specific communities
uv run python main.py preview MachineLearning
uv run python main.py preview technology

# Add interesting ones to your config
uv run python main.py setup
```

### Custom Workflow
```bash
# Quick view of config
uv run python main.py config

# Modify settings
uv run python main.py setup

# Test new feed
uv run python main.py feed
```

## 🎨 Interface

The app uses Rich library for beautiful terminal output:
- **Colorful Tables**: Easy-to-scan information
- **Progress Indicators**: Visual feedback during loading
- **Interactive Prompts**: User-friendly setup and navigation
- **Panels and Borders**: Organized, professional appearance

## 🔧 Dependencies

- **requests**: Reddit API communication
- **rich**: Terminal UI and formatting  
- **click**: Command-line interface
- **beautifulsoup4**: HTML parsing (future features)
- **python-dateutil**: Time handling

All managed by `uv` for fast, reliable dependency resolution.

## 📈 Future Enhancements

- **Saved Posts**: Bookmark interesting content
- **Notification System**: Alerts for trending topics
- **Export Features**: Save feeds to files
- **Advanced Filtering**: Machine learning content recommendation
- **Multi-platform**: GUI version with web interface
- **Social Features**: Share and discuss with friends

## 🚨 Rate Limiting

The app includes built-in rate limiting to be respectful to Reddit:
- **Delays Between Requests**: 0.5 seconds between subreddits
- **Proper User Agent**: Identifies the app appropriately
- **Error Recovery**: Handles API limits gracefully

## 🎯 Tips for Best Experience

1. **Start Small**: Begin with 5-10 subreddits
2. **Quality Over Quantity**: Set appropriate minimum scores
3. **Regular Updates**: Refresh periodically for fresh content
4. **Customize Filters**: Exclude content you don't want
5. **Explore Previews**: Test new subreddits before adding

---

**Stay informed with your personalized Reddit news feed!** 📰✨
