import pygame

from render.drawable import Drawable
from render.game_object import GameObject
from render.sprite_object import SpriteObject


class Consumable(Drawable, GameObject):
    def __init__(self, sprite_obj: SpriteObject, kind: str):
        self._sprite_obj = sprite_obj
        self.kind = kind

    @property
    def rect(self):
        return self._sprite_obj.rect

    def draw(self, screen: pygame.surface.Surface):
        self._sprite_obj.draw(screen)

    def update(self, now_ms: int) -> None:
        self._sprite_obj.update(now_ms)
