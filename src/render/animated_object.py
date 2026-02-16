from typing import Self

import pygame

from render.sprite_object import SpriteObject
from render.visual_effect import VisualEffect


class AnimatedObject(SpriteObject):
    def __init__(self, sprite: pygame.Surface | None, rect: pygame.Rect, effects: list[VisualEffect] | None = None):
        super().__init__(sprite, rect)
        self._effects = []
        if effects:
            for effect in effects:
                self._add_effect(effect)

    def update(self, dt: int) -> None:
        for effect in self._effects:
            effect.update(self, dt)

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        for effect in self._effects:
            effect.draw(screen)

    @classmethod
    def create(cls, sprite: pygame.Surface, effects: list[VisualEffect] | None = None, **kwargs) -> Self:
        assert kwargs, "Provide position"
        rect = sprite.get_rect(**kwargs)
        return cls(sprite, rect, effects)

    def _add_effect(self, effect: VisualEffect):
        effect.start(self)
        self._effects.append(effect)
