from typing import Self

import pygame

from render.sprite_object import SpriteObject
from render.visual_effect import VisualEffect


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
