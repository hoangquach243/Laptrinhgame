import pygame
from .config import *

class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, HOLE_WIDTH, HOLE_HEIGHT)
        self.occupied = False
        
    def draw(self, screen):
        # Vẽ lỗ hình oval
        # Tạo gradient effect
        pygame.draw.ellipse(screen, DARK_GRAY, self.rect)
        
        # Viền lỗ
        pygame.draw.ellipse(screen, BLACK, self.rect, 3)
        
        # Tạo hiệu ứng độ sâu
        inner_rect = pygame.Rect(self.x + 10, self.y + 8, 
                                HOLE_WIDTH - 20, HOLE_HEIGHT - 16)
        pygame.draw.ellipse(screen, BLACK, inner_rect)
        
    def is_clicked(self, pos):
        """Kiểm tra xem có click vào lỗ không"""
        return self.rect.collidepoint(pos)