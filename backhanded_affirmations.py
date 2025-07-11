#!/usr/bin/env python3
"""
Backhanded Affirmations: Daily Motivation with a Twist
An app that provides daily affirmations... with subtle shade and backhanded compliments.
Because sometimes you need encouragement that keeps you humble.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime, date
import threading
import time

class BackhandedAffirmationsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Backhanded Affirmations - Daily Motivation™")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Data file for tracking user's affirmations
        self.data_file = "affirmation_history.json"
        self.load_user_data()
        
        # Styling
        self.setup_styles()
        
        # Affirmations database (organized by categories for extra shade)
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
            ],
            "birthday": [
                "Another year older and wiser, well, definitely older!",
                "Age is just a number, and yours is getting pretty high!",
                "You're not getting older, you're getting more... experienced."
            ]
        }
        
        self.create_widgets()
        self.show_daily_affirmation()
        
    def setup_styles(self):
        """Setup custom styling for the app."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors for passive-aggressive vibes
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground='#2c3e50',
                       background='#f0f0f0')
        
        style.configure('Affirmation.TLabel',
                       font=('Georgia', 14),
                       foreground='#34495e',
                       background='#ecf0f1',
                       relief='raised',
                       padding=20)
        
        style.configure('Sassy.TButton',
                       font=('Arial', 10, 'bold'),
                       foreground='#ffffff',
                       background='#e74c3c')
        
        style.map('Sassy.TButton',
                 background=[('active', '#c0392b')])
    
    def load_user_data(self):
        """Load user's affirmation history."""
        self.user_data = {
            "total_affirmations": 0,
            "last_affirmation_date": None,
            "favorite_categories": [],
            "streak": 0,
            "achievements": []
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.user_data.update(json.load(f))
            except:
                pass  # Use defaults if file is corrupted
    
    def save_user_data(self):
        """Save user's affirmation history."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.user_data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def create_widgets(self):
        """Create the main application interface."""
        # Header
        header_frame = tk.Frame(self.root, bg='#f0f0f0')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(header_frame, 
                               text="💫 Backhanded Affirmations 💫",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Daily motivation that keeps you humble",
                                  font=('Arial', 10, 'italic'),
                                  foreground='#7f8c8d',
                                  background='#f0f0f0')
        subtitle_label.pack()
        
        # Main affirmation display
        self.affirmation_frame = tk.Frame(self.root, bg='#ecf0f1', relief='sunken', bd=2)
        self.affirmation_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.affirmation_label = ttk.Label(self.affirmation_frame,
                                          text="Loading your daily dose of reality...",
                                          style='Affirmation.TLabel',
                                          wraplength=500,
                                          justify='center')
        self.affirmation_label.pack(fill='both', expand=True)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=20, pady=10)
        
        # Buttons
        self.new_affirmation_btn = ttk.Button(button_frame,
                                             text="I Can Handle More Shade",
                                             command=self.get_new_affirmation,
                                             style='Sassy.TButton')
        self.new_affirmation_btn.pack(side='left', padx=5)
        
        self.category_btn = ttk.Button(button_frame,
                                      text="Pick My Poison",
                                      command=self.choose_category)
        self.category_btn.pack(side='left', padx=5)
        
        self.stats_btn = ttk.Button(button_frame,
                                   text="My Damage Report",
                                   command=self.show_stats)
        self.stats_btn.pack(side='left', padx=5)
        
        self.settings_btn = ttk.Button(button_frame,
                                      text="Settings",
                                      command=self.show_settings)
        self.settings_btn.pack(side='right', padx=5)
        
        # Status bar
        self.status_frame = tk.Frame(self.root, bg='#bdc3c7', height=30)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame,
                                    text="Ready to be passively motivated",
                                    bg='#bdc3c7',
                                    font=('Arial', 9))
        self.status_label.pack(expand=True)
        
        # Add menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Affirmation menu
        affirmation_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Affirmations", menu=affirmation_menu)
        affirmation_menu.add_command(label="New Affirmation", command=self.get_new_affirmation)
        affirmation_menu.add_command(label="Random Category", command=self.random_category)
        affirmation_menu.add_separator()
        affirmation_menu.add_command(label="Share the Pain", command=self.share_affirmation)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Affirmation Timer", command=self.start_timer)
        tools_menu.add_command(label="Export History", command=self.export_history)
        tools_menu.add_command(label="Reset Data", command=self.reset_data)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Manual", command=self.show_manual)
    
    def show_daily_affirmation(self):
        """Show the daily affirmation."""
        today = date.today().isoformat()
        
        # Check if we need a new daily affirmation
        if self.user_data.get("last_affirmation_date") != today:
            self.user_data["last_affirmation_date"] = today
            self.user_data["total_affirmations"] += 1
            
            # Update streak
            if self.user_data.get("last_affirmation_date"):
                # Simple streak calculation (could be more sophisticated)
                self.user_data["streak"] += 1
            else:
                self.user_data["streak"] = 1
            
            self.save_user_data()
        
        # Get special affirmation based on day or just random
        affirmation = self.get_contextual_affirmation()
        self.current_affirmation = affirmation
        
        self.update_affirmation_display(affirmation)
        self.update_status(f"Daily affirmation served • Streak: {self.user_data['streak']} days")
    
    def get_contextual_affirmation(self):
        """Get an affirmation based on context (day of week, etc.)."""
        today = datetime.now()
        day_name = today.strftime("%A").lower()
        
        # Check for special day affirmations
        if day_name == "monday" and random.random() < 0.3:
            return random.choice(self.special_affirmations["monday"])
        elif day_name == "friday" and random.random() < 0.3:
            return random.choice(self.special_affirmations["friday"])
        
        # Regular affirmation from random category
        category = random.choice(list(self.affirmations.keys()))
        return random.choice(self.affirmations[category])
    
    def get_new_affirmation(self):
        """Get a new random affirmation."""
        all_affirmations = []
        for category_affirmations in self.affirmations.values():
            all_affirmations.extend(category_affirmations)
        
        # Avoid repeating the same affirmation
        available = [a for a in all_affirmations if a != getattr(self, 'current_affirmation', '')]
        
        if available:
            affirmation = random.choice(available)
            self.current_affirmation = affirmation
            self.update_affirmation_display(affirmation)
            self.update_status("New shade delivered")
            
            self.user_data["total_affirmations"] += 1
            self.save_user_data()
    
    def choose_category(self):
        """Let user choose affirmation category."""
        category_window = tk.Toplevel(self.root)
        category_window.title("Choose Your Flavor of Motivation")
        category_window.geometry("300x400")
        category_window.configure(bg='#f0f0f0')
        
        tk.Label(category_window, 
                text="What area needs work today?",
                font=('Arial', 12, 'bold'),
                bg='#f0f0f0').pack(pady=10)
        
        for category in self.affirmations.keys():
            btn = ttk.Button(category_window,
                           text=category.replace('_', ' ').title(),
                           command=lambda c=category: self.show_category_affirmation(c, category_window))
            btn.pack(pady=5, padx=20, fill='x')
        
        # Random button
        random_btn = ttk.Button(category_window,
                              text="Surprise Me (Randomly)",
                              command=lambda: self.show_category_affirmation(None, category_window),
                              style='Sassy.TButton')
        random_btn.pack(pady=10)
    
    def show_category_affirmation(self, category, window):
        """Show affirmation from specific category."""
        window.destroy()
        
        if category is None:
            category = random.choice(list(self.affirmations.keys()))
        
        affirmation = random.choice(self.affirmations[category])
        self.current_affirmation = affirmation
        self.update_affirmation_display(affirmation)
        self.update_status(f"{category.replace('_', ' ').title()} motivation served")
        
        self.user_data["total_affirmations"] += 1
        self.save_user_data()
    
    def random_category(self):
        """Show random affirmation from random category."""
        self.show_category_affirmation(None, None)
    
    def update_affirmation_display(self, affirmation):
        """Update the main affirmation display."""
        self.affirmation_label.config(text=affirmation)
        
        # Add some visual flair
        self.affirmation_frame.config(bg=random.choice(['#ecf0f1', '#f8f9fa', '#e8f4f8']))
    
    def update_status(self, message):
        """Update status bar."""
        self.status_label.config(text=message)
        
        # Auto-clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text="Ready to be passively motivated"))
    
    def show_stats(self):
        """Show user statistics."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Your Damage Report")
        stats_window.geometry("400x300")
        stats_window.configure(bg='#f0f0f0')
        
        stats_text = f"""
📊 Your Affirmation Statistics

Total Affirmations Received: {self.user_data['total_affirmations']}
Current Streak: {self.user_data['streak']} days
Member Since: {self.user_data.get('first_use', 'Today')}

🏆 Achievements:
"""
        
        # Add some achievements based on usage
        achievements = []
        if self.user_data['total_affirmations'] >= 10:
            achievements.append("• Glutton for Punishment (10+ affirmations)")
        if self.user_data['streak'] >= 7:
            achievements.append("• Weekly Warrior (7 day streak)")
        if self.user_data['total_affirmations'] >= 50:
            achievements.append("• Masochist Level: Expert (50+ affirmations)")
        
        if not achievements:
            achievements.append("• None yet, but you're off to a... start")
        
        stats_text += "\n".join(achievements)
        
        stats_label = tk.Label(stats_window,
                              text=stats_text,
                              font=('Arial', 10),
                              justify='left',
                              bg='#f0f0f0')
        stats_label.pack(padx=20, pady=20)
    
    def show_settings(self):
        """Show settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("350x250")
        settings_window.configure(bg='#f0f0f0')
        
        tk.Label(settings_window,
                text="App Settings",
                font=('Arial', 14, 'bold'),
                bg='#f0f0f0').pack(pady=10)
        
        # Add some settings options
        ttk.Button(settings_window,
                  text="Enable Notifications (Coming Soon)",
                  state='disabled').pack(pady=5)
        
        ttk.Button(settings_window,
                  text="Export Data",
                  command=self.export_history).pack(pady=5)
        
        ttk.Button(settings_window,
                  text="Reset All Data",
                  command=self.reset_data,
                  style='Sassy.TButton').pack(pady=5)
    
    def share_affirmation(self):
        """Share current affirmation."""
        if hasattr(self, 'current_affirmation'):
            share_text = f"Today's backhanded affirmation: \"{self.current_affirmation}\" \n\n#BackhandedAffirmations #MotivationWithShade"
            
            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(share_text)
            
            messagebox.showinfo("Shared!", 
                              "Affirmation copied to clipboard!\nNow you can spread the passive-aggressive love.")
        else:
            messagebox.showwarning("Nothing to Share", 
                                 "Get an affirmation first, then share the pain.")
    
    def start_timer(self):
        """Start affirmation timer."""
        timer_window = tk.Toplevel(self.root)
        timer_window.title("Affirmation Timer")
        timer_window.geometry("300x200")
        timer_window.configure(bg='#f0f0f0')
        
        tk.Label(timer_window,
                text="Get reminded to check your ego regularly",
                font=('Arial', 11),
                bg='#f0f0f0').pack(pady=10)
        
        tk.Label(timer_window,
                text="Interval (minutes):",
                bg='#f0f0f0').pack()
        
        interval_var = tk.StringVar(value="60")
        interval_entry = tk.Entry(timer_window, textvariable=interval_var, width=10)
        interval_entry.pack(pady=5)
        
        def start_timer_thread():
            try:
                interval = int(interval_var.get()) * 60  # Convert to seconds
                timer_window.destroy()
                self.run_timer(interval)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")
        
        ttk.Button(timer_window,
                  text="Start Timer",
                  command=start_timer_thread).pack(pady=10)
    
    def run_timer(self, interval):
        """Run the affirmation timer."""
        def timer_thread():
            while True:
                time.sleep(interval)
                self.root.after(0, self.show_timer_notification)
        
        threading.Thread(target=timer_thread, daemon=True).start()
        self.update_status(f"Timer started - {interval//60} minute intervals")
    
    def show_timer_notification(self):
        """Show timer notification."""
        messagebox.showinfo("Time for Reality Check!", 
                          "Time for your scheduled dose of humble pie!\n\nClick 'I Can Handle More Shade' for a fresh affirmation.")
    
    def export_history(self):
        """Export user data."""
        try:
            export_data = {
                "export_date": datetime.now().isoformat(),
                "user_data": self.user_data,
                "sample_affirmation": getattr(self, 'current_affirmation', 'No current affirmation')
            }
            
            filename = f"backhanded_affirmations_export_{date.today().isoformat()}.json"
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            messagebox.showinfo("Export Complete", 
                              f"Data exported to {filename}\nShare your journey of humble growth!")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export data: {e}")
    
    def reset_data(self):
        """Reset all user data."""
        if messagebox.askyesno("Reset Data", 
                              "Are you sure you want to reset all your progress?\nThis will delete your streak and statistics."):
            self.user_data = {
                "total_affirmations": 0,
                "last_affirmation_date": None,
                "favorite_categories": [],
                "streak": 0,
                "achievements": []
            }
            self.save_user_data()
            messagebox.showinfo("Reset Complete", "Fresh start! Time to build a new streak of humility.")
            self.update_status("Data reset - fresh start")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
🌟 Backhanded Affirmations v1.0 🌟

Daily motivation that keeps you grounded in reality.

Created for those who prefer their encouragement 
with a side of humble pie and a sprinkle of shade.

Features:
• Daily affirmations with subtle burns
• Progress tracking (or lack thereof)
• Multiple categories of passive-aggressive support
• Timer for regular reality checks

Remember: You're doing great... for you!

© 2025 Passive-Aggressive Motivation Inc.
"Building character, one backhanded compliment at a time"
"""
        
        messagebox.showinfo("About Backhanded Affirmations", about_text)
    
    def show_manual(self):
        """Show user manual."""
        manual_text = """
📖 How to Use Backhanded Affirmations

1. Open the app (you've mastered this step!)
2. Read your daily affirmation 
3. Try not to take it personally
4. Click buttons for more constructive criticism
5. Track your progress toward self-awareness
6. Share the love (or passive aggression)

Pro Tips:
• Use the timer for regular ego checks
• Export your data to see how far you've come
• Categories help target specific areas for improvement
• Remember: It's all said with love... mostly

The app automatically saves your progress and streak.
No account required - your shame is kept locally!
"""
        
        messagebox.showinfo("User Manual", manual_text)
    
    def run(self):
        """Start the application."""
        # Set up window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set initial focus
        self.root.focus_set()
        
        # Start the main loop
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing."""
        self.save_user_data()
        self.root.quit()

def main():
    """Main function to run the app."""
    print("🌟 Starting Backhanded Affirmations...")
    print("Preparing your daily dose of passive-aggressive motivation!")
    
    app = BackhandedAffirmationsApp()
    app.run()

if __name__ == "__main__":
    main()
