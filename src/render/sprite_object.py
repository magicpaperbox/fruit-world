from typing import Self

import pygame


class SpriteObject:
    def __init__(self, sprite: pygame.Surface | None, rect: pygame.Rect):
        self._sprite = sprite
        self.rect = rect

    def draw(self, screen: pygame.surface.Surface):
        if self._sprite is not None:
            screen.blit(self._sprite, self.rect)

    def __str__(self):
        return f"SpriteObj(left: {self.rect.left}, right: {self.rect.right}, top: {self.rect.top}, bottom: {self.rect.bottom})"

    @classmethod
    def create(cls, sprite: pygame.Surface, **kwargs) -> Self:
        rect = sprite.get_rect(**kwargs)
        return cls(sprite, rect)

    @classmethod
    def create_invisible(cls, rect: pygame.Rect):
        return cls(sprite=None, rect=rect)
