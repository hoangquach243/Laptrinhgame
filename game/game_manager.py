import pygame
import random
import sys
from .config import *
from .hole import Hole
from .zombie import Zombie
from .audio_manager import AudioManager
from .ui_manager import UIManager

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zombie Whack Game - Pygame")
        self.clock = pygame.time.Clock()
        
        # Managers
        self.audio_manager = AudioManager()
        self.ui_manager = UIManager(self.screen)
        
        # Game objects
        self.holes = [Hole(x, y) for x, y in HOLE_POSITIONS]
        self.zombies = []
        
        # Game state
        self.game_state = "menu"  # menu, playing, game_over
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.time_left = GAME_TIME
        self.game_timer = 0
        self.zombie_spawn_timer = 0
        
        # Menu
        self.start_button_rect = None
        
    def spawn_zombie(self):
        """Tạo zombie mới"""
        available_holes = [hole for hole in self.holes if not hole.occupied]
        if available_holes:
            random_hole = random.choice(available_holes)
            zombie = Zombie(random_hole)
            self.zombies.append(zombie)
    
    def handle_click(self, pos):
        """Xử lý click chuột"""
        hit_zombie = False
        
        # Kiểm tra click zombie
        for zombie in self.zombies[:]:
            if zombie.is_clicked(pos):
                if zombie.hit():
                    self.score += POINTS_PER_HIT
                    self.hits += 1
                    self.audio_manager.play_sound('hit')
                    self.ui_manager.add_hit_effect(pos[0], pos[1])
                    hit_zombie = True
                    break
        
        if not hit_zombie:
            self.misses += 1
            self.audio_manager.play_sound('miss')
            self.ui_manager.add_miss_effect(pos[0], pos[1])
    
    def update_game(self, dt):
        """Cập nhật game logic"""
        if self.game_state != "playing":
            return
            
        # Cập nhật timer
        self.game_timer += dt
        self.time_left = GAME_TIME - self.game_timer // 1000
        
        if self.time_left <= 0:
            self.game_state = "game_over"
            self.audio_manager.stop_background_music()
            return
        
        # Spawn zombie
        self.zombie_spawn_timer += dt
        if self.zombie_spawn_timer >= ZOMBIE_SPAWN_RATE:
            self.spawn_zombie()
            self.zombie_spawn_timer = 0
            # Tăng tốc độ spawn theo thời gian
            spawn_rate_modifier = 1 - (self.game_timer / (GAME_TIME * 1000)) * 0.5
            self.zombie_spawn_timer = -ZOMBIE_SPAWN_RATE * (1 - spawn_rate_modifier)
        
        # Cập nhật zombies
        for zombie in self.zombies[:]:
            zombie.update(dt)
            if not zombie.alive:
                self.zombies.remove(zombie)
        
        # Cập nhật effects
        self.ui_manager.update_effects()
    
    def draw_menu(self):
        """Vẽ menu chính"""
        self.ui_manager.draw_background()
        self.ui_manager.draw_title()
        
        # Instructions
        instructions = [
            "Hướng dẫn chơi:",
            "• Click vào zombie khi chúng xuất hiện",
            "• Mỗi zombie trúng được 10 điểm",
            "• Cố gắng đạt điểm cao nhất trong 30 giây!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = YELLOW if i == 0 else WHITE
            text = self.ui_manager.font_small.render(instruction, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                                  200 + i * 30))
        
        # Start button
        mouse_pos = pygame.mouse.get_pos()
        button_x = SCREEN_WIDTH // 2 - 100
        button_y = 350
        
        hover = (button_x <= mouse_pos[0] <= button_x + 200 and 
                button_y <= mouse_pos[1] <= button_y + 50)
        
        self.start_button_rect = self.ui_manager.draw_button(
            "Bắt đầu chơi", button_x, button_y, 200, 50, 
            GREEN, WHITE, hover
        )
    
    def draw_game(self):
        """Vẽ game đang chơi"""
        self.ui_manager.draw_background()
        self.ui_manager.draw_scoreboard(self.score, self.hits, self.misses, self.time_left)
        
        # Vẽ holes
        for hole in self.holes:
            hole.draw(self.screen)
        
        # Vẽ zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Vẽ effects
        self.ui_manager.draw_effects()
    
    def draw_game_over(self):
        """Vẽ màn hình game over"""
        self.ui_manager.draw_background()
        return self.ui_manager.draw_game_over(self.score, self.hits, self.misses)
    
    def reset_game(self):
        """Reset game để chơi lại"""
        self.zombies.clear()
        for hole in self.holes:
            hole.occupied = False
        
        self.score = 0
        self.hits = 0
        self.misses = 0
        self.time_left = GAME_TIME
        self.game_timer = 0
        self.zombie_spawn_timer = 0
        
        self.ui_manager.hit_effects.clear()
        self.ui_manager.miss_effects.clear()
    
    def run(self):
        """Game loop chính"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.game_state == "menu":
                            if (self.start_button_rect and 
                                self.start_button_rect.collidepoint(event.pos)):
                                self.game_state = "playing"
                                self.reset_game()
                                self.audio_manager.play_background_music()
                        
                        elif self.game_state == "playing":
                            self.handle_click(event.pos)
                        
                        elif self.game_state == "game_over":
                            restart_button, quit_button = self.draw_game_over()
                            if restart_button.collidepoint(event.pos):
                                self.game_state = "playing"
                                self.reset_game()
                                self.audio_manager.play_background_music()
                            elif quit_button.collidepoint(event.pos):
                                running = False
            
            # Update
            self.update_game(dt)
            
            # Draw
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "playing":
                self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()