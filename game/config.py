import pygame

# Màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 90, 60)
DARK_BROWN = (93, 42, 26)

# Game settings
GAME_TIME = 30  # seconds
ZOMBIE_SHOW_TIME = 2000  # milliseconds
ZOMBIE_SPAWN_RATE = 1000  # milliseconds
POINTS_PER_HIT = 10

# Hole positions (x, y)
HOLE_POSITIONS = [
    (100, 150), (250, 130), (400, 160), (550, 140),
    (120, 250), (300, 230), (480, 270),
    (150, 350), (350, 330), (500, 360)
]

# Sizes
HOLE_WIDTH = 80
HOLE_HEIGHT = 60
ZOMBIE_WIDTH = 60
ZOMBIE_HEIGHT = 60

# Animation
ZOMBIE_RISE_SPEED = 5
ZOMBIE_FALL_SPEED = 3