import abc
from math import sin
from typing import Self

import pygame

from render.sprite_object import SpriteObject
from screen.game_units import GameUnit


class VisualEffect(abc.ABC):
    def start(self, obj: SpriteObject) -> None:
        """Is always called before any update"""
        pass

    @abc.abstractmethod
    def update(self, obj: SpriteObject, now_ms: int) -> None:
        pass


class AnimatedObject(SpriteObject):
    def __init__(self, sprite: pygame.Surface | None, rect: pygame.Rect, effects: list[VisualEffect] | None = None):
        super().__init__(sprite, rect)
        self._effects = effects
        for effect in self._effects:
            effect.start(self)

    def update(self, now_ms: int) -> None:
        for effect in self._effects:
            effect.update(self, now_ms)

    @classmethod
    def create(cls, sprite: pygame.Surface, effects: list[VisualEffect] | None = None, **kwargs) -> Self:
        assert kwargs, "Provide position"
        rect = sprite.get_rect(**kwargs)
        return cls(sprite, rect, effects)


class BobbingEffect(VisualEffect):
    def __init__(self, effect_amplitude: GameUnit, speed_factor: float):
        self._base_y = None
        self._effect_amplitude = effect_amplitude
        self._speed = speed_factor

    def start(self, obj: SpriteObject) -> None:
        self._base_y = obj.rect.y

    def update(self, obj: SpriteObject, now_ms: int) -> None:
        assert self._base_y is not None
        offset_y = int(round(sin(now_ms * self._speed) * self._effect_amplitude.pixels))
        obj.rect.y = self._base_y + offset_y
