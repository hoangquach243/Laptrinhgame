#!/usr/bin/env python3
"""
Zombie Whack Game - Pygame Version
Tác giả: Assistant
Phiên bản: 1.0

Cách chạy:
    python main.py

Yêu cầu:
    - Python 3.7+
    - pygame
    - numpy (tùy chọn, cho âm thanh synthetic)
"""

import sys
import os

# Thêm thư mục game vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_manager import GameManager

def main():
    """Hàm main chạy game"""
    try:
        print("🧟 Khởi động Zombie Whack Game...")
        print("📋 Hướng dẫn chơi:")
        print("   • Click chuột trái để đập zombie")
        print("   • Mỗi zombie trúng được 10 điểm")
        print("   • Thời gian: 30 giây")
        print("   • ESC hoặc đóng cửa sổ để thoát")
        print("-" * 50)
        
        game = GameManager()
        game.run()
        
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("🔧 Kiểm tra lại requirements.txt và thử lại")

if __name__ == "__main__":
    main()