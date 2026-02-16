import abc

import pygame

from render.drawable import Drawable
from render.sprite_object import SpriteObject


class VisualEffect(abc.ABC, Drawable):
    def start(self, obj: SpriteObject) -> None:
        pass

    @abc.abstractmethod
    def update(self, obj: SpriteObject, dt: int) -> None:
        pass

    def draw(self, screen: pygame.surface.Surface):
        pass
