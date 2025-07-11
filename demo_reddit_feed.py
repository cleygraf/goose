#!/usr/bin/env python3
"""
Reddit News Feed Demo
Demonstrates the app's capabilities without requiring full setup.
"""

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def demo_app():
    console.print("🗞️" + "=" * 60 + "🗞️")
    console.print("    REDDIT NEWS FEED DEMO")
    console.print("    Personalized News Aggregation from Reddit")
    console.print("=" * 64)
    console.print()
    
    console.print("🎯 [bold cyan]APP OVERVIEW[/bold cyan]")
    console.print("This app creates a personalized news feed by aggregating")
    console.print("content from your favorite Reddit communities (subreddits).")
    console.print()
    
    # Feature showcase
    features = [
        "✅ Multi-subreddit aggregation with smart ranking",
        "✅ Interactive browsing with post details",
        "✅ Customizable filtering (score, keywords, time)",
        "✅ Real-time updates and refresh capabilities",
        "✅ Beautiful terminal UI with Rich formatting",
        "✅ Configuration management and persistence",
        "✅ Browser integration for opening links",
        "✅ Rate-limited, respectful Reddit API usage"
    ]
    
    console.print("🚀 [bold green]KEY FEATURES:[/bold green]")
    for feature in features:
        console.print(f"  {feature}")
        time.sleep(0.3)
    
    console.print()
    
    # Sample subreddits
    console.print("📂 [bold yellow]DEFAULT SUBREDDITS:[/bold yellow]")
    subreddits = [
        ("programming", "Latest programming discussions and news"),
        ("MachineLearning", "AI/ML research and developments"),
        ("technology", "General tech news and trends"),
        ("worldnews", "Global current events"),
        ("science", "Scientific discoveries and research"),
        ("Python", "Python programming community"),
        ("datascience", "Data science and analytics"),
        ("cybersecurity", "Security news and best practices"),
        ("news", "General news and current events")
    ]
    
    sub_table = Table(box=box.ROUNDED)
    sub_table.add_column("Subreddit", style="cyan", width=20)
    sub_table.add_column("Description", style="white")
    
    for sub, desc in subreddits:
        sub_table.add_row(f"r/{sub}", desc)
    
    console.print(sub_table)
    console.print()
    
    # Sample feed simulation
    console.print("📰 [bold magenta]SAMPLE FEED OUTPUT:[/bold magenta]")
    
    # Create a mock feed table
    feed_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    feed_table.add_column("🏆", style="cyan", width=5)
    feed_table.add_column("Title", style="white", min_width=40)
    feed_table.add_column("Subreddit", style="green", width=15)
    feed_table.add_column("Score", style="yellow", justify="right", width=6)
    feed_table.add_column("Comments", style="blue", justify="right", width=8)
    feed_table.add_column("Author", style="dim", width=12)
    feed_table.add_column("Age", style="dim", width=8)
    
    # Sample posts
    sample_posts = [
        ("🥇", "Breaking: Major AI Breakthrough in Language Models", "MachineLearning", "2.1k", "324", "researcher_ai", "2h"),
        ("🥈", "Python 3.13 Release Candidate Now Available", "Python", "1.8k", "156", "python_dev", "4h"),
        ("🥉", "Cybersecurity Alert: New Zero-Day Vulnerability", "cybersecurity", "1.5k", "203", "sec_expert", "1h"),
        ("4", "NASA Discovers Water on Mars Surface", "science", "3.2k", "567", "space_news", "6h"),
        ("5", "Tech Giants Report Q3 Earnings Beat Expectations", "technology", "987", "89", "tech_analyst", "3h"),
        ("6", "New Data Science Framework Speeds ML Training", "datascience", "756", "124", "ds_researcher", "5h"),
        ("7", "Global Climate Summit Reaches Historic Agreement", "worldnews", "4.1k", "892", "environment", "8h"),
        ("8", "Revolutionary Programming Language Announced", "programming", "634", "167", "lang_creator", "7h"),
    ]
    
    for rank, title, subreddit, score, comments, author, age in sample_posts:
        feed_table.add_row(rank, title, f"r/{subreddit}", score, comments, author, age)
    
    feed_panel = Panel(
        feed_table,
        title="📰 Your Personalized Reddit Feed (8 posts)",
        subtitle="Updated: 2025-07-11 13:30:00",
        border_style="bright_blue"
    )
    
    console.print(feed_panel)
    console.print()
    
    # Command examples
    console.print("💻 [bold cyan]COMMAND EXAMPLES:[/bold cyan]")
    commands = [
        ("./launch.sh", "Quick start - launch the main feed"),
        ("uv run python main.py feed", "Show your personalized feed"),
        ("uv run python main.py setup", "Interactive configuration setup"),
        ("uv run python main.py preview technology", "Preview posts from specific subreddit"),
        ("uv run python main.py config", "Show current settings"),
        ("uv run python main.py feed --setup", "Setup while viewing feed")
    ]
    
    cmd_table = Table(box=box.ROUNDED)
    cmd_table.add_column("Command", style="green", width=35)
    cmd_table.add_column("Description", style="white")
    
    for cmd, desc in commands:
        cmd_table.add_row(cmd, desc)
    
    console.print(cmd_table)
    console.print()
    
    # Interactive features
    console.print("🎮 [bold yellow]INTERACTIVE FEATURES:[/bold yellow]")
    interactive_features = [
        "📖 Browse posts by number (1, 2, 3, etc.)",
        "🔄 Refresh feed with 'r' command",
        "🌐 Open URLs or Reddit comments in browser",
        "⚙️ Customize subreddits and filters",
        "📊 View post details and content previews",
        "🎯 Filter by score, time, and keywords",
        "💾 Save configuration preferences",
        "🚫 Exclude unwanted content automatically"
    ]
    
    for feature in interactive_features:
        console.print(f"  {feature}")
        time.sleep(0.2)
    
    console.print()
    
    # Configuration demo
    console.print("⚙️ [bold green]CUSTOMIZATION OPTIONS:[/bold green]")
    console.print("""
[cyan]Sort Options:[/cyan] hot, new, top, rising
[cyan]Time Filters:[/cyan] hour, day, week, month, year, all
[cyan]Score Filtering:[/cyan] Hide posts below minimum score
[cyan]Keyword Exclusion:[/cyan] Filter out unwanted terms
[cyan]Post Limits:[/cyan] Control feed size and subreddit balance
[cyan]Topic Focus:[/cyan] Curate subreddits for your interests
    """)
    
    # Usage tips
    console.print("💡 [bold magenta]PRO TIPS:[/bold magenta]")
    tips = [
        "Start with default subreddits, then customize based on your interests",
        "Use 'preview' command to test new subreddits before adding them",
        "Set minimum score (10+) to filter out low-quality content",
        "Exclude keywords like 'spoiler' to avoid unwanted content",
        "Refresh regularly to stay current with trending topics",
        "Use browser integration to dive deeper into interesting posts"
    ]
    
    for i, tip in enumerate(tips, 1):
        console.print(f"  {i}. {tip}")
        time.sleep(0.3)
    
    console.print()
    
    console.print("🚀 [bold green]READY TO START?[/bold green]")
    console.print("Run [cyan]./launch.sh[/cyan] to launch your personalized Reddit news feed!")
    console.print()
    
    console.print("🔗 [bold blue]COMMANDS TO TRY:[/bold blue]")
    console.print("  [green]uv run python main.py preview programming[/green]")
    console.print("  [green]uv run python main.py setup[/green]") 
    console.print("  [green]uv run python main.py feed[/green]")
    console.print()
    
    console.print("📊 [bold yellow]SAMPLE WORKFLOW:[/bold yellow]")
    workflow = [
        "1. 📋 Run setup to configure your interests",
        "2. 🔍 Preview subreddits to test content quality", 
        "3. 📰 Launch main feed to see aggregated results",
        "4. 📖 Browse posts interactively with numbers",
        "5. 🌐 Open interesting links in your browser",
        "6. 🔄 Refresh periodically for fresh content"
    ]
    
    for step in workflow:
        console.print(f"  {step}")
        time.sleep(0.2)
    
    console.print()
    console.print("🌟 [bold cyan]Stay informed with personalized Reddit news![/bold cyan] 🌟")
    console.print("=" * 64)

if __name__ == "__main__":
    demo_app()
