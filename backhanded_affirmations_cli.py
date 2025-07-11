#!/usr/bin/env python3
"""
Backhanded Affirmations - Command Line Version
A passive-aggressive motivation app that works in any terminal.
Perfect for when you need a reality check but don't have GUI access.
"""

import random
import json
import os
from datetime import datetime, date
import argparse

class BackhandedAffirmationsCLI:
    def __init__(self):
        self.data_file = "affirmation_history_cli.json"
        self.load_user_data()
        
        # Same snarky affirmations as the GUI version
        self.affirmations = {
            "motivation": [
                "You're doing your best, which I assume is what that was.",
                "Every failure is just practice for your next disappointment!",
                "You're unique, just like everyone else trying their hardest.",
                "Today you'll accomplish something, probably.",
                "Your potential is limitless, unlike your current achievements.",
                "You're not behind in life, everyone else is just showing off.",
                "You're perfectly average, and that's... something!",
                "Your dreams are valid, even if they seem impossible right now.",
                "You're growing every day, mostly horizontally, but still growing.",
                "You matter, at least to your internet service provider."
            ],
            "confidence": [
                "You're beautiful on the inside, which is what counts when the outside needs work.",
                "You have a face for radio and a voice for silent films!",
                "You're not like other people, and some might consider that a warning.",
                "You light up every room you enter, mostly because people turn on lights to see who came in.",
                "Your personality really makes up for a lot of things.",
                "You're unforgettable, like a car accident or food poisoning.",
                "You have such a wonderful sense of humor about yourself.",
                "You're aging gracefully, considering the circumstances.",
                "You're so genuine, people always know exactly what they're getting.",
                "You're the main character in your own story, which explains a lot."
            ],
            "success": [
                "Success is just around the corner, it's been hiding there for a while now.",
                "You're exactly where you need to be, which hopefully isn't your parents' basement.",
                "Your hard work will pay off eventually, assuming compound interest applies to effort.",
                "You're on the right path, even if it's the scenic route through failure.",
                "Great things take time, and you're really taking your time.",
                "You're building character, which is free and apparently abundant.",
                "Your journey is unique, like a fingerprint or a trainwreck.",
                "You're learning so much from your mistakes, you must be very wise by now.",
                "Persistence pays off, and you've certainly been persistent.",
                "You're meant for great things, we're just not sure what those are yet."
            ],
            "relationships": [
                "You're loved for who you are, flaws and all, mostly all.",
                "Someone out there is perfect for you, they just haven't lowered their standards yet.",
                "You're a catch, assuming someone's fishing in the right pond.",
                "Your friends appreciate your honesty, when they ask for it.",
                "You bring out the best in people, usually by comparison.",
                "You're irreplaceable, mainly because no one else would do what you do.",
                "People remember you fondly, eventually.",
                "You're a great listener, probably because you don't talk much.",
                "You're loyal to a fault, literally to a fault.",
                "You make people feel better about themselves just by being you."
            ],
            "self_care": [
                "You deserve rest, your productivity levels certainly suggest you've been getting it.",
                "Self-care isn't selfish, it's self-preservation for everyone around you.",
                "You're enough, assuming 'enough' has very flexible standards.",
                "Take time for yourself, everyone else seems to have figured that out.",
                "You deserve good things, and you usually get what you deserve.",
                "Love yourself, someone has to.",
                "You're worth the effort, minimal though it may be.",
                "Treat yourself with kindness, it's probably the only kindness you'll get today.",
                "You're doing important work, even if it's not immediately obvious what that is.",
                "Your mental health matters, to your therapist's mortgage payments."
            ]
        }
        
        # Special occasion affirmations
        self.special_affirmations = {
            "monday": [
                "Monday is a fresh start, to make the same mistakes with renewed vigor!",
                "You're ready to tackle this Monday, assuming Monday doesn't tackle back.",
                "New week, same you, but with slightly more optimism!"
            ],
            "friday": [
                "You've survived another week, congratulations on your continued existence!",
                "TGIF - Thank Goodness I'm Functional, barely but still.",
                "You've earned this weekend, mostly through sheer persistence."
            ]
        }
    
    def load_user_data(self):
        """Load user's affirmation history."""
        self.user_data = {
            "total_affirmations": 0,
            "last_affirmation_date": None,
            "streak": 0,
            "categories_used": [],
            "favorite_affirmations": []
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.user_data.update(json.load(f))
            except:
                pass
    
    def save_user_data(self):
        """Save user's affirmation history."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.user_data, f, default=str, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving data: {e}")
    
    def get_daily_affirmation(self):
        """Get the daily affirmation."""
        today = date.today().isoformat()
        
        # Check if we need a new daily affirmation
        if self.user_data.get("last_affirmation_date") != today:
            self.user_data["last_affirmation_date"] = today
            self.user_data["total_affirmations"] += 1
            
            # Update streak
            self.user_data["streak"] += 1
            
            self.save_user_data()
        
        # Get contextual affirmation
        return self.get_contextual_affirmation()
    
    def get_contextual_affirmation(self):
        """Get affirmation based on context."""
        today = datetime.now()
        day_name = today.strftime("%A").lower()
        
        # Special day affirmations
        if day_name == "monday" and random.random() < 0.3:
            return random.choice(self.special_affirmations["monday"])
        elif day_name == "friday" and random.random() < 0.3:
            return random.choice(self.special_affirmations["friday"])
        
        # Regular affirmation
        category = random.choice(list(self.affirmations.keys()))
        return random.choice(self.affirmations[category])
    
    def get_category_affirmation(self, category):
        """Get affirmation from specific category."""
        if category in self.affirmations:
            affirmation = random.choice(self.affirmations[category])
            self.user_data["total_affirmations"] += 1
            if category not in self.user_data["categories_used"]:
                self.user_data["categories_used"].append(category)
            self.save_user_data()
            return affirmation
        else:
            return "Invalid category. Your reading comprehension needs work too."
    
    def show_stats(self):
        """Display user statistics."""
        print("\n📊 YOUR DAMAGE REPORT:")
        print("=" * 40)
        print(f"Total Affirmations Received: {self.user_data['total_affirmations']}")
        print(f"Current Streak: {self.user_data['streak']} days")
        print(f"Categories Explored: {len(self.user_data['categories_used'])}/5")
        
        # Achievements
        achievements = []
        if self.user_data['total_affirmations'] >= 10:
            achievements.append("🏆 Glutton for Punishment (10+ affirmations)")
        if self.user_data['streak'] >= 7:
            achievements.append("🏆 Weekly Warrior (7 day streak)")
        if len(self.user_data['categories_used']) >= 5:
            achievements.append("🏆 Category Completist (tried all categories)")
        
        if achievements:
            print("\n🎖️ Achievements Unlocked:")
            for achievement in achievements:
                print(f"   {achievement}")
        else:
            print("\n🎖️ Achievements: None yet, but you're trying!")
        print()
    
    def list_categories(self):
        """List available categories."""
        print("\n📂 AVAILABLE CATEGORIES:")
        print("=" * 30)
        for i, category in enumerate(self.affirmations.keys(), 1):
            print(f"{i}. {category.replace('_', ' ').title()}")
        print()
    
    def interactive_mode(self):
        """Run interactive command-line interface."""
        print("🌟 BACKHANDED AFFIRMATIONS - INTERACTIVE MODE 🌟")
        print("Type 'help' for commands, 'exit' to quit")
        print()
        
        # Show daily affirmation first
        daily = self.get_daily_affirmation()
        print("💬 YOUR DAILY AFFIRMATION:")
        print(f"   \"{daily}\"")
        print()
        
        while True:
            try:
                command = input("🤔 What kind of motivation do you need? > ").strip().lower()
                
                if command in ['exit', 'quit', 'q']:
                    print("👋 Thanks for using Backhanded Affirmations!")
                    print("Remember: You're doing your best... probably! 💫")
                    break
                
                elif command in ['help', 'h']:
                    self.show_help()
                
                elif command in ['new', 'random', 'r']:
                    affirmation = self.get_contextual_affirmation()
                    print(f"\n💬 \"{affirmation}\"\n")
                    self.user_data["total_affirmations"] += 1
                    self.save_user_data()
                
                elif command in ['categories', 'cat', 'c']:
                    self.list_categories()
                
                elif command in ['stats', 'status', 's']:
                    self.show_stats()
                
                elif command.isdigit():
                    category_index = int(command) - 1
                    categories = list(self.affirmations.keys())
                    if 0 <= category_index < len(categories):
                        category = categories[category_index]
                        affirmation = self.get_category_affirmation(category)
                        print(f"\n💬 {category.replace('_', ' ').title()}: \"{affirmation}\"\n")
                    else:
                        print("❌ Invalid category number. Try 'categories' to see options.\n")
                
                elif command in self.affirmations:
                    affirmation = self.get_category_affirmation(command)
                    print(f"\n💬 {command.replace('_', ' ').title()}: \"{affirmation}\"\n")
                
                else:
                    print("❓ Unknown command. Type 'help' for options.\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Fine, be that way! See you next time.")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
    
    def show_help(self):
        """Show available commands."""
        print("\n📖 AVAILABLE COMMANDS:")
        print("=" * 30)
        print("• 'new' or 'random' - Get a random affirmation")
        print("• 'categories' or 'c' - List available categories")
        print("• '1-5' or category name - Get category-specific affirmation")
        print("• 'stats' - Show your progress")
        print("• 'help' - Show this help")
        print("• 'exit' - Quit app")
        print()

def main():
    parser = argparse.ArgumentParser(description="Backhanded Affirmations - CLI Version")
    parser.add_argument('--daily', action='store_true', help='Show daily affirmation and exit')
    parser.add_argument('--category', '-c', help='Get affirmation from specific category')
    parser.add_argument('--random', '-r', action='store_true', help='Get random affirmation and exit')
    parser.add_argument('--stats', '-s', action='store_true', help='Show statistics and exit')
    parser.add_argument('--list', '-l', action='store_true', help='List categories and exit')
    
    args = parser.parse_args()
    
    app = BackhandedAffirmationsCLI()
    
    if args.daily:
        affirmation = app.get_daily_affirmation()
        print(f"📅 Daily Affirmation: \"{affirmation}\"")
    
    elif args.random:
        affirmation = app.get_contextual_affirmation()
        print(f"💬 Random Affirmation: \"{affirmation}\"")
        app.user_data["total_affirmations"] += 1
        app.save_user_data()
    
    elif args.category:
        if args.category in app.affirmations:
            affirmation = app.get_category_affirmation(args.category)
            print(f"💬 {args.category.replace('_', ' ').title()}: \"{affirmation}\"")
        else:
            print(f"❌ Unknown category '{args.category}'. Available: {', '.join(app.affirmations.keys())}")
    
    elif args.stats:
        app.show_stats()
    
    elif args.list:
        app.list_categories()
    
    else:
        # Interactive mode
        app.interactive_mode()

if __name__ == "__main__":
    main()
