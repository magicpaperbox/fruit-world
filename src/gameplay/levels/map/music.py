import pygame


class Music:
    def __init__(self):
        self._current_music_path: str | None = None

    def play(self, music_path: str):
        if music_path != self._current_music_path:
            self._current_music_path = music_path
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
