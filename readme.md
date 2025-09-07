# 🧟 Zombie Whack Game - Pygame Version

Game đập đầu zombie được viết bằng Python Pygame với đầy đủ tính năng theo yêu cầu BTL1.

## 🎯 Tính năng

### Phần bắt buộc (9 điểm):
✅ **Thiết kế hình nền với nhiều chỗ xuất hiện zombie (2đ)**
- 10 lỗ được bố trí khác nhau trên màn hình
- Background gradient đẹp mắt
- Hiệu ứng độ sâu cho các lỗ

✅ **Có thiết kế zombie (1đ)**  
- Zombie với đầu tròn màu nâu
- Mắt đỏ, răng trắng, miệng đen
- Animation mượt mà

✅ **Vẽ hình đầu zombie với timer (2đ)**
- Zombie xuất hiện ngẫu nhiên 
- Tự động biến mất sau 2-3 giây
- Timer đếm ngược 30 giây

✅ **Tương tác được với chuột (3đ)**
- Phát hiện click chính xác tại vị trí (x,y)
- Xác định chính xác khi click trúng zombie
- Collision detection với pygame.Rect

✅ **Output điểm số hoàn chỉnh (2đ)**
- Đếm số lần đập trúng và miss
- Hiển thị tỷ lệ chính xác (%)
- Scoreboard real-time

### Phần thưởng (bonus):
🎵 **Âm thanh**
- Sound effects khi hit/miss
- Background music (nếu có file)
- Synthetic audio nếu không có file âm thanh

✨ **Hiệu ứng visual** 
- Animation zombie lên xuống
- Hiệu ứng đỏ khi đập trúng
- Text "MISS!" khi bắn trượt
- Button hover effects

🎮 **Tính năng bổ sung**
- Menu chính với hướng dẫn
- Game over screen với stats
- Restart game không cần thoát
- Tốc độ tăng dần theo thời gian

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống:
- Python 3.7 trở lên
- Pygame 2.0+
- Numpy (tùy chọn, cho synthetic audio)

### Cài đặt:
```bash
# Clone hoặc download project
git clone <repository-url>
cd zombie-whack-pygame

# Cài đặt dependencies  
pip install -r requirements.txt

# Chạy game
python main.py