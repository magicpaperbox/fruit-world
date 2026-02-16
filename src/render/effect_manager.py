import pygame

from render.drawable import Drawable
from render.game_object import GameObject
from render.sprite_object import SpriteObject
from render.visual_effect import VisualEffect


class EffectManager(Drawable, GameObject):
    def __init__(self):
        self._effects: list[tuple[SpriteObject, VisualEffect]] = []

    def add_effect(self, effect: VisualEffect, position: tuple[float, float]):
        rect = pygame.Rect(position, (0, 0))
        sprite_obj = SpriteObject(sprite=None, rect=rect)
        effect.start(sprite_obj)
        self._effects.append((sprite_obj, effect))

    def draw(self, screen: pygame.surface.Surface):
        for _, effect in self._effects:
            effect.draw(screen)

    def update(self, dt: int):
        for obj, effect in self._effects:
            effect.update(obj, dt)
