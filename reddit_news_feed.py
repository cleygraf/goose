#!/usr/bin/env python3
"""
Personalized Reddit News Feed
Aggregates content from Reddit based on user interests and topics.
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.prompt import Prompt, Confirm
from rich import box
import time
import webbrowser

console = Console()

class RedditNewsFeed:
    def __init__(self, config_file: str = "feed_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.base_url = "https://www.reddit.com"
        self.session = requests.Session()
        # Use a proper user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'PersonalizedNewsFeed/1.0 (Educational Purpose)'
        })
        
    def load_config(self) -> Dict:
        """Load user configuration for topics and preferences."""
        default_config = {
            "topics": [
                "technology", "programming", "python", "artificial_intelligence",
                "science", "worldnews", "news", "datascience", "cybersecurity"
            ],
            "subreddits": [
                "programming", "MachineLearning", "technology", "worldnews",
                "science", "Python", "datascience", "cybersecurity", "news"
            ],
            "time_filter": "day",  # day, week, month, year, all
            "sort_by": "hot",      # hot, new, top, rising
            "max_posts_per_sub": 5,
            "max_total_posts": 25,
            "auto_refresh_minutes": 30,
            "show_preview": True,
            "save_read_posts": True,
            "keywords_filter": [],
            "exclude_keywords": ["spoiler", "NSFW"],
            "minimum_score": 10,
            "last_update": None
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure new keys are present
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                console.print(f"[red]Error loading config: {e}[/red]")
                
        return default_config
    
    def save_config(self):
        """Save current configuration."""
        self.config["last_update"] = datetime.now().isoformat()
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving config: {e}[/red]")
    
    def fetch_subreddit_posts(self, subreddit: str, limit: int = 25) -> List[Dict]:
        """Fetch posts from a specific subreddit."""
        try:
            url = f"{self.base_url}/r/{subreddit}/{self.config['sort_by']}.json"
            params = {
                'limit': limit,
                't': self.config['time_filter']
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                
                # Filter by score
                if post_data.get('score', 0) < self.config['minimum_score']:
                    continue
                
                # Filter by keywords
                title_lower = post_data.get('title', '').lower()
                if self.config['exclude_keywords']:
                    if any(keyword.lower() in title_lower for keyword in self.config['exclude_keywords']):
                        continue
                
                posts.append({
                    'title': post_data.get('title', 'No title'),
                    'url': post_data.get('url', ''),
                    'permalink': f"{self.base_url}{post_data.get('permalink', '')}",
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'created_utc': post_data.get('created_utc', 0),
                    'author': post_data.get('author', 'unknown'),
                    'subreddit': post_data.get('subreddit', subreddit),
                    'id': post_data.get('id', ''),
                    'selftext': post_data.get('selftext', ''),
                    'thumbnail': post_data.get('thumbnail', ''),
                    'is_self': post_data.get('is_self', False)
                })
            
            return posts[:self.config['max_posts_per_sub']]
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching r/{subreddit}: {e}[/red]")
            return []
        except Exception as e:
            console.print(f"[red]Error processing r/{subreddit}: {e}[/red]")
            return []
    
    def fetch_all_posts(self) -> List[Dict]:
        """Fetch posts from all configured subreddits."""
        all_posts = []
        
        with console.status(f"[bold green]Fetching from {len(self.config['subreddits'])} subreddits..."):
            for i, subreddit in enumerate(self.config['subreddits']):
                console.print(f"[cyan]Fetching r/{subreddit}... ({i+1}/{len(self.config['subreddits'])})[/cyan]")
                posts = self.fetch_subreddit_posts(subreddit)
                all_posts.extend(posts)
                time.sleep(0.5)  # Be nice to Reddit's servers
        
        # Sort by score and creation time
        all_posts.sort(key=lambda x: (x['score'], x['created_utc']), reverse=True)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_posts = []
        for post in all_posts:
            if post['url'] not in seen_urls:
                seen_urls.add(post['url'])
                unique_posts.append(post)
        
        return unique_posts[:self.config['max_total_posts']]
    
    def display_posts(self, posts: List[Dict]):
        """Display posts in a nice formatted table."""
        if not posts:
            console.print("[yellow]No posts found matching your criteria.[/yellow]")
            return
        
        # Create a table
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("🏆", style="cyan", width=5)
        table.add_column("Title", style="white", min_width=40)
        table.add_column("Subreddit", style="green", width=15)
        table.add_column("Score", style="yellow", justify="right", width=6)
        table.add_column("Comments", style="blue", justify="right", width=8)
        table.add_column("Author", style="dim", width=12)
        table.add_column("Age", style="dim", width=8)
        
        for i, post in enumerate(posts, 1):
            # Calculate post age
            post_time = datetime.fromtimestamp(post['created_utc'])
            age = self.format_time_ago(post_time)
            
            # Truncate title if too long
            title = post['title']
            if len(title) > 60:
                title = title[:57] + "..."
            
            # Truncate author name
            author = post['author']
            if len(author) > 10:
                author = author[:7] + "..."
            
            # Add trophy emoji for top posts
            rank_emoji = "🥇" if i <= 3 else "🏅" if i <= 10 else str(i)
            
            table.add_row(
                rank_emoji,
                title,
                f"r/{post['subreddit']}",
                str(post['score']),
                str(post['num_comments']),
                author,
                age
            )
        
        # Create a panel with the table
        panel = Panel(
            table,
            title=f"📰 Your Personalized Reddit Feed ({len(posts)} posts)",
            subtitle=f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="bright_blue"
        )
        
        console.print(panel)
    
    def format_time_ago(self, post_time: datetime) -> str:
        """Format time difference in a readable way."""
        now = datetime.now()
        diff = now - post_time
        
        if diff.days > 0:
            return f"{diff.days}d"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}h"
        else:
            minutes = diff.seconds // 60
            return f"{minutes}m"
    
    def interactive_setup(self):
        """Interactive setup for first-time users."""
        console.print("\n[bold yellow]🚀 Welcome to Reddit News Feed![/bold yellow]")
        console.print("Let's set up your personalized feed.\n")
        
        # Get user interests
        console.print("[cyan]What topics are you interested in?[/cyan]")
        console.print("Current topics:", ", ".join(self.config['topics']))
        
        if Confirm.ask("Do you want to customize your topics?"):
            new_topics = []
            console.print("\n[dim]Enter topics one by one (press Enter on empty line to finish):[/dim]")
            while True:
                topic = Prompt.ask("Topic", default="")
                if not topic:
                    break
                new_topics.append(topic)
            
            if new_topics:
                self.config['topics'] = new_topics
        
        # Get subreddits
        console.print(f"\n[cyan]Current subreddits:[/cyan] {', '.join(self.config['subreddits'])}")
        
        if Confirm.ask("Do you want to customize your subreddits?"):
            new_subs = []
            console.print("\n[dim]Enter subreddit names one by one (without r/):[/dim]")
            while True:
                sub = Prompt.ask("Subreddit", default="")
                if not sub:
                    break
                new_subs.append(sub.replace('r/', '').strip())
            
            if new_subs:
                self.config['subreddits'] = new_subs
        
        # Other preferences
        sort_options = ["hot", "new", "top", "rising"]
        time_options = ["hour", "day", "week", "month", "year", "all"]
        
        self.config['sort_by'] = Prompt.ask(
            "Sort posts by", 
            choices=sort_options, 
            default=self.config['sort_by']
        )
        
        self.config['time_filter'] = Prompt.ask(
            "Time filter", 
            choices=time_options, 
            default=self.config['time_filter']
        )
        
        self.config['max_total_posts'] = int(Prompt.ask(
            "Maximum posts to show", 
            default=str(self.config['max_total_posts'])
        ))
        
        self.config['minimum_score'] = int(Prompt.ask(
            "Minimum post score", 
            default=str(self.config['minimum_score'])
        ))
        
        self.save_config()
        console.print("\n[green]✅ Configuration saved![/green]")
    
    def show_config(self):
        """Display current configuration."""
        config_table = Table(title="📋 Current Configuration", box=box.ROUNDED)
        config_table.add_column("Setting", style="cyan", min_width=20)
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Subreddits", ", ".join(self.config['subreddits']))
        config_table.add_row("Sort by", self.config['sort_by'])
        config_table.add_row("Time filter", self.config['time_filter'])
        config_table.add_row("Max posts", str(self.config['max_total_posts']))
        config_table.add_row("Min score", str(self.config['minimum_score']))
        config_table.add_row("Exclude keywords", ", ".join(self.config['exclude_keywords']))
        
        console.print(config_table)
    
    def interactive_menu(self, posts: List[Dict]):
        """Interactive menu for browsing posts."""
        if not posts:
            return
        
        while True:
            console.print(f"\n[bold cyan]📖 Browse Posts (1-{len(posts)}, 'q' to quit, 'r' to refresh)[/bold cyan]")
            
            choice = Prompt.ask("Enter post number or command").strip().lower()
            
            if choice == 'q':
                break
            elif choice == 'r':
                console.print("[yellow]Refreshing feed...[/yellow]")
                return 'refresh'
            elif choice.isdigit():
                post_num = int(choice) - 1
                if 0 <= post_num < len(posts):
                    self.show_post_details(posts[post_num])
                else:
                    console.print(f"[red]Invalid post number. Please enter 1-{len(posts)}[/red]")
            else:
                console.print(f"[red]Invalid choice. Enter a number (1-{len(posts)}), 'r' to refresh, or 'q' to quit.[/red]")
    
    def show_post_details(self, post: Dict):
        """Show detailed view of a post."""
        console.clear()
        
        # Create post details panel
        details = f"""
[bold]{post['title']}[/bold]

[cyan]Subreddit:[/cyan] r/{post['subreddit']}
[cyan]Author:[/cyan] u/{post['author']}
[cyan]Score:[/cyan] {post['score']} | [cyan]Comments:[/cyan] {post['num_comments']}
[cyan]Posted:[/cyan] {self.format_time_ago(datetime.fromtimestamp(post['created_utc']))} ago

[cyan]URL:[/cyan] {post['url']}
[cyan]Reddit:[/cyan] {post['permalink']}
"""
        
        if post['selftext'] and not post['is_self']:
            details += f"\n[cyan]Content:[/cyan]\n{post['selftext'][:300]}..."
        
        panel = Panel(details, title="📖 Post Details", border_style="green")
        console.print(panel)
        
        # Options
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Open URL in browser")
        console.print("2. Open Reddit comments")
        console.print("3. Copy URL")
        console.print("4. Back to list")
        
        choice = Prompt.ask("Choose option", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1" and post['url']:
            webbrowser.open(post['url'])
            console.print("[green]Opened in browser![/green]")
        elif choice == "2":
            webbrowser.open(post['permalink'])
            console.print("[green]Opened Reddit comments![/green]")
        elif choice == "3":
            # Simple copy to clipboard (requires additional setup for cross-platform)
            console.print(f"[yellow]URL: {post['url']}[/yellow]")
            console.print("[dim]Copy the URL above[/dim]")
        
        if choice in ["1", "2", "3"]:
            Prompt.ask("\nPress Enter to continue")

@click.group()
def cli():
    """🗞️ Personalized Reddit News Feed - Stay updated with your interests!"""
    pass

@cli.command()
@click.option('--setup', is_flag=True, help='Run interactive setup')
@click.option('--config', is_flag=True, help='Show current configuration')
def feed(setup, config):
    """📰 Show your personalized Reddit news feed."""
    app = RedditNewsFeed()
    
    if setup:
        app.interactive_setup()
        return
    
    if config:
        app.show_config()
        return
    
    # Main feed display
    console.print("[bold green]🚀 Loading your personalized Reddit feed...[/bold green]")
    
    try:
        while True:
            posts = app.fetch_all_posts()
            console.clear()
            app.display_posts(posts)
            
            result = app.interactive_menu(posts)
            if result != 'refresh':
                break
                
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Thanks for using Reddit News Feed![/yellow]")

@cli.command()
def setup():
    """⚙️ Interactive setup for your news feed preferences."""
    app = RedditNewsFeed()
    app.interactive_setup()

@cli.command()
def config():
    """📋 Show current configuration."""
    app = RedditNewsFeed()
    app.show_config()

@cli.command()
@click.argument('subreddit')
@click.option('--limit', default=10, help='Number of posts to fetch')
def preview(subreddit, limit):
    """🔍 Preview posts from a specific subreddit."""
    app = RedditNewsFeed()
    console.print(f"[cyan]Fetching posts from r/{subreddit}...[/cyan]")
    
    posts = app.fetch_subreddit_posts(subreddit, limit)
    if posts:
        # Create a simple preview table
        table = Table(title=f"📋 r/{subreddit} Preview", box=box.ROUNDED)
        table.add_column("Title", style="white", min_width=50)
        table.add_column("Score", style="yellow", justify="right")
        table.add_column("Comments", style="blue", justify="right")
        
        for post in posts:
            title = post['title'][:60] + "..." if len(post['title']) > 60 else post['title']
            table.add_row(title, str(post['score']), str(post['num_comments']))
        
        console.print(table)
    else:
        console.print(f"[red]No posts found in r/{subreddit}[/red]")

if __name__ == "__main__":
    cli()
