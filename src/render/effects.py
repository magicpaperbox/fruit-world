from math import sin

import pygame

from render.sprite_object import Collectible


class VisualEffects:
    def __init__(self, collectible: Collectible):
        self._collectible = collectible
        self._effect_amplitude: int = 8
        self._speed: float = 0.003
        self.base_y: int = collectible.rect.y

    def bobbing(self, now_ms: int):
        offset_y = sin(now_ms * self._speed) * self._effect_amplitude
        self._collectible.rect.y = int(self.base_y + offset_y)

    def update(self, now_ms: int):
        if self._collectible.kind == "heart":
            self.bobbing(now_ms)