import pygame
import random
import os

class MusicController:
    def __init__(self, music_dir="music"):
        self.music_dir = music_dir
        self.playlist = []
        self.current_index = 0
        self.paused = False
        
        pygame.mixer.init()
        self._load_playlist()
    
    def _load_playlist(self):
        extensions = ['.mp3', '.wav', '.ogg']
        if os.path.exists(self.music_dir):
            for f in os.listdir(self.music_dir):
                if any(f.lower().endswith(ext) for ext in extensions):
                    self.playlist.append(os.path.join(self.music_dir, f))
    
    def play_music(self):
        if self.playlist:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.load(self.playlist[self.current_index])
                pygame.mixer.music.play()
                self.paused = False
            return os.path.basename(self.playlist[self.current_index])
        return None
    
    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            return os.path.basename(self.playlist[self.current_index])
        return None
    
    def next_music(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            pygame.mixer.music.stop()
            return self.play_music()
        return None
    
    def previous_music(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            pygame.mixer.music.stop()
            return self.play_music()
        return None
    
    def random_play(self):
        if self.playlist:
            self.current_index = random.randint(0, len(self.playlist) - 1)
            pygame.mixer.music.stop()
            return self.play_music()
        return None

