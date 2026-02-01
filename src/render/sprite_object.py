from typing import Self

import pygame

from render.drawable import Drawable
from render.game_object import GameObject


class SpriteObject(Drawable, GameObject):
    def __init__(self, sprite: pygame.Surface | None, rect: pygame.Rect):
        self._sprite = sprite
        self.rect = rect

    def update(self, now_ms: int):
        pass

    def draw(self, screen: pygame.surface.Surface):
        if self._sprite is not None:
            screen.blit(self._sprite, self.rect)

    def __str__(self):
        return f"SpriteObj(left: {self.rect.left}, right: {self.rect.right}, top: {self.rect.top}, bottom: {self.rect.bottom})"

    @classmethod
    def create(cls, sprite: pygame.Surface, **kwargs) -> Self:
        assert kwargs, "Provide position"
        rect = sprite.get_rect(**kwargs)
        return cls(sprite, rect)

    @classmethod
    def create_invisible(cls, rect: pygame.Rect):
        return cls(sprite=None, rect=rect)
