import pygame
import random
from .config import *

class Zombie:
    zombie_img = None  # Khởi tạo biến class
    def __init__(self, hole):
        if Zombie.zombie_img is None:
            Zombie.zombie_img = pygame.image.load("assets/images/zombie.png").convert_alpha()
        self.hole = hole
        self.x = hole.x + (HOLE_WIDTH - ZOMBIE_WIDTH) // 2
        self.y = hole.y + HOLE_HEIGHT  # Bắt đầu ở dưới lỗ
        self.target_y = hole.y - 10  # Vị trí khi xuất hiện
        self.rect = pygame.Rect(self.x, self.y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT)
        
        # Trạng thái
        self.state = "rising"  # rising, showing, falling, dead
        self.alive = True
        self.show_time = 0
        self.max_show_time = ZOMBIE_SHOW_TIME + random.randint(-500, 500)
        
        # Animation
        self.rise_speed = ZOMBIE_RISE_SPEED
        self.fall_speed = ZOMBIE_FALL_SPEED
        
        # Đánh dấu lỗ bị chiếm
        hole.occupied = True
        
    def update(self, dt):
        """Cập nhật trạng thái zombie"""
        if not self.alive:
            return
            
        if self.state == "rising":
            self.y -= self.rise_speed
            if self.y <= self.target_y:
                self.y = self.target_y
                self.state = "showing"
                self.show_time = 0
                
        elif self.state == "showing":
            self.show_time += dt
            if self.show_time >= self.max_show_time:
                self.state = "falling"
                
        elif self.state == "falling":
            self.y += self.fall_speed
            if self.y >= self.hole.y + HOLE_HEIGHT:
                self.alive = False
                self.hole.occupied = False
                
        # Cập nhật rect
        self.rect.y = self.y
        
    def draw(self, screen):
        """Vẽ zombie"""
        screen.blit(Zombie.zombie_img, (self.x, self.y))
        if not self.alive or self.y >= self.hole.y + HOLE_HEIGHT:
            return
            
        # Vẽ đầu zombie (hình tròn)
        head_center = (self.x + ZOMBIE_WIDTH // 2, 
                      int(self.y) + ZOMBIE_HEIGHT // 2)
        
        # Đầu zombie màu nâu
        pygame.draw.circle(screen, BROWN, head_center, ZOMBIE_WIDTH // 2)
        pygame.draw.circle(screen, DARK_BROWN, head_center, ZOMBIE_WIDTH // 2, 3)
        
        # Mắt đỏ
        eye_size = 6
        left_eye = (head_center[0] - 12, head_center[1] - 8)
        right_eye = (head_center[0] + 12, head_center[1] - 8)
        pygame.draw.circle(screen, RED, left_eye, eye_size)
        pygame.draw.circle(screen, RED, right_eye, eye_size)
        
        # Mắt đen (con ngươi)
        pygame.draw.circle(screen, BLACK, left_eye, 3)
        pygame.draw.circle(screen, BLACK, right_eye, 3)
        
        # Miệng
        mouth_rect = pygame.Rect(head_center[0] - 8, head_center[1] + 5, 16, 8)
        pygame.draw.ellipse(screen, BLACK, mouth_rect)
        
        # Răng
        for i in range(3):
            tooth_x = head_center[0] - 6 + i * 4
            tooth_y = head_center[1] + 6
            pygame.draw.polygon(screen, WHITE, [
                (tooth_x, tooth_y),
                (tooth_x + 2, tooth_y),
                (tooth_x + 1, tooth_y + 4)
            ])
    
    def is_clicked(self, pos):
        """Kiểm tra xem có click trúng zombie không"""
        if not self.alive or self.state != "showing":
            return False
        return self.rect.collidepoint(pos)
    
    def hit(self):
        """Zombie bị đập"""
        if self.alive and self.state == "showing":
            self.state = "falling"
            self.fall_speed = ZOMBIE_FALL_SPEED * 2  # Rơi nhanh hơn khi bị đập
            return True
        return False