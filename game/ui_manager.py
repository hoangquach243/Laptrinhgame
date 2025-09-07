import pygame
from .config import *

class UIManager:
    def __init__(self, screen):
        self.background_img = pygame.transform.scale(
    pygame.image.load("assets/images/background.png").convert(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Tạo các surfaces cho hiệu ứng
        self.hit_effects = []
        self.miss_effects = []
        
    def draw_background(self):
        """Vẽ background gradient"""
        self.screen.blit(self.background_img, (0, 0))
        # Tạo gradient từ xanh đậm đến đen
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            color = (
                int(26 * (1 - ratio)),  # R
                int(26 * (1 - ratio)),  # G  
                int(46 * (1 - ratio))   # B
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_title(self):
        """Vẽ tiêu đề game"""
        title_text = self.font_large.render("🧟 ZOMBIE WHACK GAME 🧟", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        
        # Shadow effect
        shadow_text = self.font_large.render("🧟 ZOMBIE WHACK GAME 🧟", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 2, 52))
        
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
    
    def draw_scoreboard(self, score, hits, misses, time_left):
        """Vẽ bảng điểm"""
        # Background cho scoreboard
        scoreboard_rect = pygame.Rect(50, 80, SCREEN_WIDTH - 100, 60)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), scoreboard_rect)
        pygame.draw.rect(self.screen, WHITE, scoreboard_rect, 2)
        
        # Tính tỷ lệ chính xác
        total_shots = hits + misses
        accuracy = (hits / total_shots * 100) if total_shots > 0 else 0
        
        # Các thông tin
        score_text = f"Điểm: {score}"
        hits_text = f"Trúng: {hits}"
        misses_text = f"Trượt: {misses}"
        accuracy_text = f"Chính xác: {accuracy:.1f}%"
        time_text = f"Thời gian: {time_left}s"
        
        # Vị trí vẽ text
        texts = [score_text, hits_text, misses_text, accuracy_text, time_text]
        x_positions = [80, 200, 320, 440, 600]
        
        for i, (text, x_pos) in enumerate(zip(texts, x_positions)):
            color = YELLOW if i == 4 and time_left <= 10 else WHITE
            if i == 4 and time_left <= 10:  # Nhấp nháy khi sắp hết thời gian
                color = RED if (pygame.time.get_ticks() // 500) % 2 else YELLOW
            
            rendered_text = self.font_small.render(text, True, color)
            self.screen.blit(rendered_text, (x_pos, 100))
    
    def draw_button(self, text, x, y, width, height, color, text_color, hover=False):
        """Vẽ button"""
        button_color = tuple(min(255, c + 30) for c in color) if hover else color
        button_rect = pygame.Rect(x, y, width, height)
        
        # Shadow
        shadow_rect = pygame.Rect(x + 3, y + 3, width, height)
        pygame.draw.rect(self.screen, DARK_GRAY, shadow_rect, border_radius=10)
        
        # Button
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, button_rect, 3, border_radius=10)
        
        # Text
        button_text = self.font_medium.render(text, True, text_color)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        return button_rect
    
    def add_hit_effect(self, x, y):
        """Thêm hiệu ứng khi hit"""
        self.hit_effects.append({
            'x': x,
            'y': y,
            'radius': 10,
            'max_radius': 50,
            'alpha': 255,
            'time': pygame.time.get_ticks()
        })
    
    def add_miss_effect(self, x, y):
        """Thêm hiệu ứng khi miss"""
        self.miss_effects.append({
            'x': x,
            'y': y,
            'text': 'MISS!',
            'alpha': 255,
            'y_offset': 0,
            'time': pygame.time.get_ticks()
        })
    
    def update_effects(self):
        """Cập nhật các hiệu ứng"""
        current_time = pygame.time.get_ticks()
        
        # Cập nhật hit effects
        for effect in self.hit_effects[:]:
            elapsed = current_time - effect['time']
            if elapsed > 500:  # 0.5 seconds
                self.hit_effects.remove(effect)
            else:
                progress = elapsed / 500
                effect['radius'] = effect['max_radius'] * progress
                effect['alpha'] = int(255 * (1 - progress))
        
        # Cập nhật miss effects  
        for effect in self.miss_effects[:]:
            elapsed = current_time - effect['time']
            if elapsed > 1000:  # 1 second
                self.miss_effects.remove(effect)
            else:
                progress = elapsed / 1000
                effect['y_offset'] = -30 * progress
                effect['alpha'] = int(255 * (1 - progress))
    
    def draw_effects(self):
        """Vẽ các hiệu ứng"""
        # Vẽ hit effects
        for effect in self.hit_effects:
            if effect['alpha'] > 0:
                # Tạo surface với alpha
                surf = pygame.Surface((effect['radius'] * 2, effect['radius'] * 2), pygame.SRCALPHA)
                color = (*RED, effect['alpha'])
                pygame.draw.circle(surf, color, 
                                 (effect['radius'], effect['radius']), 
                                 effect['radius'])
                self.screen.blit(surf, (effect['x'] - effect['radius'], 
                                      effect['y'] - effect['radius']))
        
        # Vẽ miss effects
        for effect in self.miss_effects:
            if effect['alpha'] > 0:
                miss_text = self.font_medium.render(effect['text'], True, 
                                                   (*RED, effect['alpha']))
                self.screen.blit(miss_text, (effect['x'] - 30, 
                                           effect['y'] + effect['y_offset']))
    
    def draw_game_over(self, final_score, hits, misses):
        """Vẽ màn hình game over"""
        # Overlay đen trong suốt
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Box game over
        box_width, box_height = 400, 300
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = (SCREEN_HEIGHT - box_height) // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        pygame.draw.rect(self.screen, DARK_GRAY, box_rect, border_radius=15)
        pygame.draw.rect(self.screen, WHITE, box_rect, 3, border_radius=15)
        
        # Text
        title = self.font_large.render("GAME OVER!", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, box_y + 60))
        
        total_shots = hits + misses
        accuracy = (hits / total_shots * 100) if total_shots > 0 else 0
        
        score_text = self.font_medium.render(f"Điểm cuối: {final_score}", True, WHITE)
        accuracy_text = self.font_medium.render(f"Độ chính xác: {accuracy:.1f}%", True, WHITE)
        stats_text = self.font_small.render(f"Trúng: {hits} | Trượt: {misses}", True, WHITE)
        
        self.screen.blit(title, title_rect)
        self.screen.blit(score_text, (box_x + 50, box_y + 120))
        self.screen.blit(accuracy_text, (box_x + 50, box_y + 150))
        self.screen.blit(stats_text, (box_x + 50, box_y + 180))
        
        # Button chơi lại
        restart_button = self.draw_button("Chơi lại", box_x + 50, box_y + 220, 120, 40, 
                                        GREEN, WHITE)
        quit_button = self.draw_button("Thoát", box_x + 200, box_y + 220, 120, 40, 
                                     RED, WHITE)
        
        return restart_button, quit_button