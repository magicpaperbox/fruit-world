import pygame

from render.game_object import GameObject


class Animation(GameObject):
    def __init__(self, duration: int, frames: list[pygame.Surface]):
        self.sprite = frames[0]
        self._duration = duration
        self._frames = frames
        self._current_game_frame = 0
        self._frame_index = 0

    def update(self, dt_ms: int):
        self._current_game_frame += dt_ms
        if self._current_game_frame >= self._duration:
            self._current_game_frame -= self._duration
            if self._frame_index == len(self._frames) - 1:
                self._frame_index = 0
            else:
                self._frame_index += 1
            self.sprite = self._frames[self._frame_index]

    def surface(self) -> pygame.Surface:
        return self._frames[self._frame_index]
