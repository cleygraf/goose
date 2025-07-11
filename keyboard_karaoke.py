"""
Keyboard Karaoke: Spy Theme Edition
An interactive rhythm game where users press random keys to progress through a spy-themed melody.
"""

import pygame
import random
import time
import sys
import math
from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class KeyboardKaraoke:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Display settings
        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Keyboard Karaoke: Spy Theme Edition")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_RED = (139, 0, 0)
        
        # Game state
        self.state = GameState.MENU
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Spy theme melody (original composition inspired by spy movies)
        # Notes represented as frequencies (Hz)
        self.melody = [
            (392, 0.25),  # G4 - short
            (392, 0.25),  # G4 - short
            (392, 0.25),  # G4 - short
            (370, 0.75),  # F#4 - long
            (330, 0.25),  # E4 - short
            (392, 0.25),  # G4 - short
            (330, 0.25),  # E4 - short
            (277, 1.0),   # C#4 - very long
            (330, 0.5),   # E4 - medium
            (370, 0.5),   # F#4 - medium
            (392, 0.25),  # G4 - short
            (440, 0.25),  # A4 - short
            (494, 0.75),  # B4 - long
            (523, 0.5),   # C5 - medium
            (494, 1.5),   # B4 - extra long
            (392, 0.25),  # G4 - short
            (440, 0.25),  # A4 - short
            (370, 0.5),   # F#4 - medium
            (330, 1.0),   # E4 - long
        ]
        
        # Key progression
        self.required_keys = []
        self.generate_key_sequence()
        
        # Game variables
        self.current_note = 0
        self.current_key_index = 0
        self.score = 0
        self.accuracy = 100.0
        self.total_presses = 0
        self.correct_presses = 0
        self.start_time = 0
        self.note_start_time = 0
        self.is_playing_note = False
        self.current_channel = None
        
        # Visual effects
        self.particles = []
        self.key_display_time = {}
        
    def generate_key_sequence(self):
        """Generate a sequence of random keys for the user to press."""
        keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Generate 3-4 keys per note
        for note in self.melody:
            num_keys = random.randint(3, 4)
            for _ in range(num_keys):
                self.required_keys.append(random.choice(keys))
    
    def generate_tone(self, frequency, duration):
        """Generate a sine wave tone."""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        for i in range(frames):
            wave = 32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate)
            arr.append([int(wave), int(wave)])
        return pygame.sndarray.make_sound(arr)
    
    def play_note(self, frequency, duration):
        """Play a musical note."""
        if self.current_channel:
            self.current_channel.stop()
        
        sound = self.generate_tone(frequency, duration)
        self.current_channel = sound.play()
        return sound
    
    def add_particle(self, x, y, color):
        """Add a visual particle effect."""
        for _ in range(5):
            particle = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'vx': random.randint(-3, 3),
                'vy': random.randint(-5, -1),
                'color': color,
                'life': 30
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Update particle animations."""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_menu(self):
        """Draw the main menu."""
        self.screen.fill(self.BLACK)
        
        # Title
        title = self.font_large.render("KEYBOARD KARAOKE", True, self.WHITE)
        subtitle = self.font_medium.render("SPY THEME EDITION", True, self.YELLOW)
        
        title_rect = title.get_rect(center=(self.width // 2, 150))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 200))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        instructions = [
            "Mission: Help the spy complete their theme song!",
            "Press the displayed keys in sequence to progress the melody.",
            "Each correct key press advances the music.",
            "Miss too many and the mission fails!",
            "",
            "Press SPACE to start your mission",
            "Press ESC to abort mission"
        ]
        
        y_offset = 280
        for instruction in instructions:
            if instruction:
                text = self.font_small.render(instruction, True, self.WHITE)
                text_rect = text.get_rect(center=(self.width // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_game(self):
        """Draw the main game interface."""
        self.screen.fill(self.BLACK)
        
        # Progress bar
        progress = min(self.current_note / len(self.melody), 1.0)
        bar_width = self.width - 100
        bar_height = 20
        bar_x = 50
        bar_y = 50
        
        pygame.draw.rect(self.screen, self.GRAY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, self.GREEN, (bar_x, bar_y, bar_width * progress, bar_height))
        
        progress_text = self.font_small.render(f"Mission Progress: {progress * 100:.1f}%", True, self.WHITE)
        self.screen.blit(progress_text, (bar_x, bar_y + 25))
        
        # Current key to press
        if self.current_key_index < len(self.required_keys):
            current_key = self.required_keys[self.current_key_index]
            key_text = self.font_large.render(f"Press: {current_key}", True, self.YELLOW)
            key_rect = key_text.get_rect(center=(self.width // 2, 200))
            self.screen.blit(key_text, key_rect)
            
            # Pulsing effect
            pulse = abs(math.sin(time.time() * 5)) * 50
            pygame.draw.circle(self.screen, (255, 255, int(pulse)), key_rect.center, 80, 3)
        
        # Score and stats
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.WHITE)
        accuracy_text = self.font_medium.render(f"Accuracy: {self.accuracy:.1f}%", True, self.WHITE)
        
        self.screen.blit(score_text, (50, 100))
        self.screen.blit(accuracy_text, (50, 130))
        
        # Recent key presses display
        y_pos = 300
        for key, timestamp in list(self.key_display_time.items()):
            if time.time() - timestamp < 1.0:  # Show for 1 second
                alpha = int(255 * (1.0 - (time.time() - timestamp)))
                color = (alpha, alpha, alpha)
                key_surface = self.font_small.render(f"Pressed: {key}", True, color)
                self.screen.blit(key_surface, (self.width - 200, y_pos))
                y_pos += 25
            else:
                del self.key_display_time[key]
        
        # Particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 30))
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(self.screen, particle['color'], (int(particle['x']), int(particle['y'])), 3)
        
        # Instructions
        instruction_text = self.font_small.render("Press P to pause, ESC to quit", True, self.GRAY)
        self.screen.blit(instruction_text, (10, self.height - 30))
    
    def draw_game_over(self):
        """Draw the game over screen."""
        self.screen.fill(self.BLACK)
        
        if self.current_note >= len(self.melody):
            # Mission accomplished
            title = self.font_large.render("MISSION ACCOMPLISHED!", True, self.GREEN)
            subtitle = self.font_medium.render("The spy theme has been completed!", True, self.WHITE)
        else:
            # Mission failed
            title = self.font_large.render("MISSION FAILED", True, self.RED)
            subtitle = self.font_medium.render("The spy couldn't complete their theme...", True, self.WHITE)
        
        title_rect = title.get_rect(center=(self.width // 2, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 250))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Final stats
        final_score = self.font_medium.render(f"Final Score: {self.score}", True, self.WHITE)
        final_accuracy = self.font_medium.render(f"Final Accuracy: {self.accuracy:.1f}%", True, self.WHITE)
        
        score_rect = final_score.get_rect(center=(self.width // 2, 320))
        accuracy_rect = final_accuracy.get_rect(center=(self.width // 2, 350))
        
        self.screen.blit(final_score, score_rect)
        self.screen.blit(final_accuracy, accuracy_rect)
        
        # Restart option
        restart_text = self.font_small.render("Press SPACE to start new mission, ESC to quit", True, self.YELLOW)
        restart_rect = restart_text.get_rect(center=(self.width // 2, 450))
        self.screen.blit(restart_text, restart_rect)
    
    def handle_key_press(self, key):
        """Handle user key presses."""
        if self.state != GameState.PLAYING:
            return
        
        self.total_presses += 1
        self.key_display_time[key] = time.time()
        
        if self.current_key_index < len(self.required_keys):
            expected_key = self.required_keys[self.current_key_index]
            
            if key == expected_key:
                # Correct key pressed
                self.correct_presses += 1
                self.score += 10
                self.current_key_index += 1
                
                # Add visual effect
                self.add_particle(self.width // 2, 200, self.GREEN)
                
                # Check if we should advance to next note
                keys_per_note = len(self.required_keys) // len(self.melody)
                if self.current_key_index % keys_per_note == 0 and self.current_note < len(self.melody):
                    # Play next note
                    if self.current_note < len(self.melody):
                        frequency, duration = self.melody[self.current_note]
                        self.play_note(frequency, duration)
                        self.current_note += 1
                        self.note_start_time = time.time()
                
                # Check if mission is complete
                if self.current_note >= len(self.melody):
                    self.state = GameState.GAME_OVER
            else:
                # Wrong key pressed
                self.score = max(0, self.score - 5)
                self.add_particle(self.width // 2, 200, self.RED)
        
        # Update accuracy
        if self.total_presses > 0:
            self.accuracy = (self.correct_presses / self.total_presses) * 100
        
        # Check for mission failure
        if self.accuracy < 50 and self.total_presses > 10:
            self.state = GameState.GAME_OVER
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.current_note = 0
        self.current_key_index = 0
        self.score = 0
        self.accuracy = 100.0
        self.total_presses = 0
        self.correct_presses = 0
        self.particles = []
        self.key_display_time = {}
        self.required_keys = []
        self.generate_key_sequence()
        self.start_time = time.time()
        if self.current_channel:
            self.current_channel.stop()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.MENU
                        else:
                            running = False
                    
                    elif event.key == pygame.K_SPACE:
                        if self.state == GameState.MENU or self.state == GameState.GAME_OVER:
                            self.reset_game()
                            self.state = GameState.PLAYING
                    
                    elif event.key == pygame.K_p:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.PAUSED
                        elif self.state == GameState.PAUSED:
                            self.state = GameState.PLAYING
                    
                    elif self.state == GameState.PLAYING:
                        # Handle game keys
                        key_name = pygame.key.name(event.key).upper()
                        if len(key_name) == 1:  # Only single character keys
                            self.handle_key_press(key_name)
            
            # Update game state
            if self.state == GameState.PLAYING:
                self.update_particles()
            
            # Draw everything
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.PAUSED:
                self.draw_game()
                # Pause overlay
                pause_text = self.font_large.render("PAUSED", True, self.YELLOW)
                pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
                pygame.draw.rect(self.screen, self.BLACK, pause_rect.inflate(40, 20))
                self.screen.blit(pause_text, pause_rect)
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = KeyboardKaraoke()
    game.run()
