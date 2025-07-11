#!/usr/bin/env python3
"""
Backhanded Affirmations Demo
Show off the app's passive-aggressive motivational content without needing GUI.
"""

import random
import time

def demo_affirmations():
    print("🌟" + "=" * 60 + "🌟")
    print("    BACKHANDED AFFIRMATIONS DEMO")
    print("    Daily Motivation That Keeps You Humble")
    print("=" * 64)
    print()
    
    # Sample affirmations by category
    demo_affirmations = {
        "💪 Motivation": [
            "You're doing your best, which I assume is what that was.",
            "Every failure is just practice for your next disappointment!",
            "Your potential is limitless, unlike your current achievements.",
            "You're growing every day, mostly horizontally, but still growing."
        ],
        "😎 Confidence": [
            "You're beautiful on the inside, which is what counts when the outside needs work.",
            "You light up every room you enter, mostly because people turn on lights to see who came in.",
            "You're unforgettable, like a car accident or food poisoning.",
            "You're the main character in your own story, which explains a lot."
        ],
        "🏆 Success": [
            "Success is just around the corner, it's been hiding there for a while now.",
            "Great things take time, and you're really taking your time.",
            "You're on the right path, even if it's the scenic route through failure.",
            "You're meant for great things, we're just not sure what those are yet."
        ],
        "❤️ Relationships": [
            "Someone out there is perfect for you, they just haven't lowered their standards yet.",
            "You bring out the best in people, usually by comparison.",
            "You make people feel better about themselves just by being you.",
            "You're loyal to a fault, literally to a fault."
        ],
        "🧘 Self-Care": [
            "Love yourself, someone has to.",
            "You deserve good things, and you usually get what you deserve.",
            "Self-care isn't selfish, it's self-preservation for everyone around you.",
            "Your mental health matters, to your therapist's mortgage payments."
        ]
    }
    
    # Special occasion samples
    special_samples = {
        "📅 Monday Motivation": [
            "Monday is a fresh start, to make the same mistakes with renewed vigor!",
            "New week, same you, but with slightly more optimism!"
        ],
        "🎉 Friday Feel-Good": [
            "You've survived another week, congratulations on your continued existence!",
            "You've earned this weekend, mostly through sheer persistence."
        ]
    }
    
    print("🎯 SAMPLE AFFIRMATIONS BY CATEGORY:\n")
    
    for category, affirmations in demo_affirmations.items():
        print(f"{category}")
        print("-" * 40)
        for affirmation in affirmations[:2]:  # Show 2 per category
            print(f"   • \"{affirmation}\"")
        print(f"   ... and {len(affirmations)-2} more gems!")
        print()
    
    print("🎪 SPECIAL OCCASION AFFIRMATIONS:\n")
    
    for occasion, affirmations in special_samples.items():
        print(f"{occasion}")
        print("-" * 40)
        for affirmation in affirmations:
            print(f"   • \"{affirmation}\"")
        print()
    
    print("🛠️  APP FEATURES DEMONSTRATION:\n")
    
    features = [
        "✅ 30+ backhanded compliments across 5 categories",
        "✅ Daily streak tracking (for consistency masochists)",
        "✅ Smart context (Monday blues, Friday relief)",
        "✅ Timer notifications for regular reality checks",
        "✅ Share function to spread the passive-aggressive love",
        "✅ Statistics dashboard to track your humble growth",
        "✅ Data export for therapeutic documentation",
        "✅ Cross-platform GUI with snarky styling"
    ]
    
    for feature in features:
        print(f"  {feature}")
        time.sleep(0.5)  # Dramatic pause
    
    print("\n" + "🎮 INTERACTIVE SIMULATION:" + "\n")
    print("👆 User clicks 'I Can Handle More Shade'")
    time.sleep(1)
    print(f"💬 App responds: \"{random.choice(demo_affirmations['💪 Motivation'])}\"")
    time.sleep(1)
    print("📊 Stats updated: Total affirmations: 42, Streak: 7 days")
    time.sleep(1)
    print("🏆 Achievement unlocked: 'Glutton for Punishment'")
    print()
    
    print("🚀 TO RUN THE FULL APP:")
    print("  ./launch_affirmations.sh")
    print("  OR")
    print("  python3 backhanded_affirmations.py")
    print()
    
    print("⚠️  DISCLAIMER:")
    print("This app provides lighthearted, humorous motivation.")
    print("All affirmations are meant in good fun and gentle teasing.")
    print("Not recommended for those sensitive to sarcasm!")
    print()
    
    print("😏 TESTIMONIALS:")
    testimonials = [
        "\"Finally, affirmations that match my self-esteem!\" - Anonymous User",
        "\"I love how it keeps me grounded in reality.\" - Hopeful Dreamer",
        "\"My therapist loves the data export feature.\" - Frequent User",
        "\"It's like having a sassy best friend in app form.\" - Comedy Lover"
    ]
    
    for testimonial in testimonials:
        print(f"  {testimonial}")
        time.sleep(1)
    
    print()
    print("🌟 Ready to start your journey of humble self-improvement? 🌟")
    print("=" * 64)

if __name__ == "__main__":
    demo_affirmations()
