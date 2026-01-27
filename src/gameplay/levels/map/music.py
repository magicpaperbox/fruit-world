import pygame


class Music:
    def __init__(self, music: str | None):
        self.music = music

    def play(self, music_path):
        if music_path != self.music:
            self.music = music_path
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
