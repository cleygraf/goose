# Keyboard Karaoke: Spy Theme Edition 🕵️‍♂️

A thrilling keyboard rhythm game where you help a spy complete their mission by playing an original spy-themed melody through precise key presses!

## 🎯 Mission Objective

Press the correct sequence of random keys to progress through an epic spy theme song. Each correct key press advances the melody, but miss too many and the mission fails!

## 🎮 How to Play

1. **Launch the Game**: Run the Python script to start your mission
2. **Read Your Orders**: The main menu explains your mission
3. **Start Playing**: Press SPACE to begin
4. **Follow Instructions**: Press the displayed keys in the correct sequence
5. **Complete the Mission**: Reach the end of the spy theme to win!

## 🎵 Game Features

### Audio System
- **Original Spy Theme**: An exciting 19-note melody inspired by classic spy movie themes
- **Real-time Audio**: Each correct key sequence triggers the next part of the melody
- **Dynamic Progression**: Music advances only when you press the correct keys

### Visual Effects
- **Mission Progress Bar**: Track your advancement through the song
- **Particle Effects**: Visual feedback for correct (green) and incorrect (red) key presses
- **Pulsing Key Display**: The required key pulses to grab your attention
- **Live Statistics**: Real-time score and accuracy tracking

### Game Mechanics
- **Random Key Sequences**: Each playthrough generates different key combinations
- **Accuracy Tracking**: Maintain at least 50% accuracy or the mission fails
- **Progressive Difficulty**: 3-4 random keys required per musical note
- **Score System**: +10 points for correct keys, -5 points for mistakes

## 🎮 Controls

| Key | Action |
|-----|---------|
| **Letters A-Z** | Game input keys |
| **Numbers 0-9** | Game input keys |
| **SPACE** | Start game / Restart after game over |
| **P** | Pause/Resume during gameplay |
| **ESC** | Return to menu / Quit game |

## 📋 Requirements

- Python 3.6+
- Pygame library

## 🚀 Quick Start

### Option 1: Smart Launcher (Recommended)
```bash
# Automatically detects capabilities and launches best version
./launch_karaoke_smart.sh
```

### Option 2: Manual Launch
```bash
# Full version (requires numpy for rich audio)
./launch_karaoke.sh
# OR
source venv/bin/activate && python keyboard_karaoke.py

# Lightweight version (pygame only - simplified audio)
source venv/bin/activate && python keyboard_karaoke_light.py
```

## 🎵 Game Versions

### Full Version (`keyboard_karaoke.py`)
- **Rich Audio**: Real-time sine wave synthesis with complex harmonics
- **Requirements**: Python 3.6+, pygame, numpy
- **Best Experience**: High-quality musical notes with precise timing

### Lightweight Version (`keyboard_karaoke_light.py`)
- **Simplified Audio**: Basic beep sounds for maximum compatibility
- **Requirements**: Python 3.6+, pygame (no numpy needed)
- **Wider Compatibility**: Works on systems where numpy is difficult to install

Both versions offer the same gameplay experience with identical features:
- ✅ Original spy-themed melody
- ✅ Random key sequences  
- ✅ Visual effects and particle system
- ✅ Score tracking and accuracy measurement
- ✅ All game states and controls

## 🏆 Winning Conditions

- **Mission Accomplished**: Successfully press all key sequences to complete the spy theme
- **Mission Failed**: Accuracy drops below 50% or you quit mid-mission

## 🎨 Game States

1. **Main Menu**: Mission briefing and start options
2. **Playing**: Active gameplay with music and key prompts  
3. **Paused**: Temporary halt (press P to resume)
4. **Game Over**: Mission results and restart option

## 🔧 Technical Features

- **Cross-platform**: Runs on Windows, macOS, and Linux
- **60 FPS Gameplay**: Smooth animations and responsive controls
- **Real-time Audio Generation**: Synthesized musical notes
- **Dynamic Key Generation**: Randomized sequences for replayability
- **Visual Feedback System**: Particles and UI updates

## 🎯 Tips for Success

1. **Focus on the Current Key**: Don't try to read ahead
2. **Maintain Rhythm**: Listen to the music for timing cues
3. **Stay Calm**: Panic leads to mistakes
4. **Practice Makes Perfect**: Each playthrough has different keys
5. **Use Both Hands**: Spread your fingers across the keyboard

## 🎼 Original Spy Theme Composition

The game features an original 19-note melody composed specifically for this game, inspired by the tension and excitement of classic spy movie themes. The melody includes:

- Dynamic tempo changes
- Ascending and descending sequences  
- Dramatic pauses and sustained notes
- Classic spy movie chord progressions

## 🚀 Future Enhancement Ideas

- Multiple difficulty levels
- Different music themes (action, stealth, chase scenes)
- Multiplayer competitive mode
- Custom song import
- Advanced visual effects
- Leaderboard system

## 🕵️‍♂️ Mission Briefing

*Agent, your mission, should you choose to accept it, is to complete the spy theme melody by pressing the correct key sequences. The fate of the musical world depends on your keyboarding skills. This message will self-destruct in... well, it won't, but you get the idea.*

**Good luck, Agent!** 🎖️

---

*Created as part of the Goose AI workshop demonstration*
