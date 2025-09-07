"""
Zombie Whack Game Package

Game đập đầu zombie được viết bằng Python Pygame
"""

__version__ = "1.0.0"
__author__ = "Assistant"

# Import main classes
from .game_manager import GameManager
from .zombie import Zombie
from .hole import Hole
from .audio_manager import AudioManager
from .ui_manager import UIManager

__all__ = [
    'GameManager',
    'Zombie', 
    'Hole',
    'AudioManager',
    'UIManager'
]