import pygame
import os

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("🔊 Audio system initialized")
        except:
            print("🔇 Audio system failed, running silent")
        
        self.sounds = {}
        self.background_music = None
        self.audio_enabled = True
        self.load_sounds()
        
    def load_sounds(self):
        """Load âm thanh từ file hoặc tạo dummy"""
        sound_files = {
            'hit': 'assets/sounds/hit.wav',
            'miss': 'assets/sounds/miss.wav',
            'background': 'assets/sounds/background.mp3'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    if name == 'background':
                        self.background_music = path
                    else:
                        self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"✅ Loaded sound: {name}")
                except pygame.error as e:
                    print(f"❌ Cannot load {path}: {e}")
                    self.create_dummy_sound(name)
            else:
                # File không tồn tại, tạo dummy
                self.create_dummy_sound(name)
    
    def create_dummy_sound(self, sound_name):
        """Tạo dummy sound object"""
        try:
            # Tạo silent sound bằng cách tạo file tạm
            import tempfile
            import wave
            import struct
            
            # Tạo file WAV tạm thời
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Tạo file WAV silent
            sample_rate = 22050
            duration = 0.1 if sound_name == 'hit' else 0.2
            num_samples = int(sample_rate * duration)
            
            with wave.open(temp_filename, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Tạo dữ liệu âm thanh đơn giản
                for i in range(num_samples):
                    # Tạo âm thanh rất nhỏ thay vì silent
                    if sound_name == 'hit':
                        # Âm thanh hit: frequency cao giảm dần
                        freq = 800 * (1 - i / num_samples)
                        amplitude = 1000 * (1 - i / num_samples)
                    else:
                        # Âm thanh miss: frequency thấp
                        freq = 150
                        amplitude = 500 * (1 - i / num_samples)
                    
                    import math
                    sample = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
                    wav_file.writeframes(struct.pack('<h', sample))
            
            # Load file WAV
            self.sounds[sound_name] = pygame.mixer.Sound(temp_filename)
            
            # Xóa file tạm
            os.unlink(temp_filename)
            
            print(f"✅ Created synthetic sound: {sound_name}")
            
        except Exception as e:
            print(f"❌ Cannot create sound {sound_name}: {e}")
            # Fallback: tạo object dummy
            self.sounds[sound_name] = DummySound()
    
    def play_sound(self, sound_name):
        """Phát âm thanh"""
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except Exception as e:
            # Ignore audio errors silently
            pass
    
    def play_background_music(self):
        """Phát nhạc nền"""
        if self.background_music and os.path.exists(self.background_music):
            try:
                pygame.mixer.music.load(self.background_music)
                pygame.mixer.music.play(-1)  # Loop vô hạn
                pygame.mixer.music.set_volume(0.3)
                print("🎵 Background music started")
            except pygame.error as e:
                print(f"❌ Cannot play background music: {e}")
    
    def stop_background_music(self):
        """Dừng nhạc nền"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def set_volume(self, volume):
        """Đặt âm lượng (0.0 - 1.0)"""
        try:
            for sound in self.sounds.values():
                if hasattr(sound, 'set_volume'):
                    sound.set_volume(volume)
        except:
            pass

class DummySound:
    """Dummy sound object khi không tạo được âm thanh thật"""
    def play(self):
        pass
    
    def set_volume(self, volume):
        pass
    
    def stop(self):
        pass