import abc
from typing import Self

import pygame

from gameplay.levels.object_spec import ConsumableSpec
from gameplay.player.player import Player
from render.drawable import Drawable
from render.effect_manager import EffectManager
from render.game_object import GameObject
from render.sprite_object import SpriteObject


class Consumable(Drawable, GameObject, abc.ABC):
    def __init__(self, sprite_obj: SpriteObject):
        self._sprite_obj = sprite_obj

    @property
    def rect(self):
        return self._sprite_obj.rect

    def draw(self, screen: pygame.surface.Surface):
        self._sprite_obj.draw(screen)

    def update(self, dt: int) -> None:
        self._sprite_obj.update(dt)

    @abc.abstractmethod
    def on_consume(self, player: Player, effect_manager: EffectManager):
        pass

    @classmethod
    @abc.abstractmethod
    def from_spec(cls, obj_spec: ConsumableSpec) -> Self:
        pass

    @staticmethod
    def consume(consumables: list["Consumable"], player: Player, effect_manager: EffectManager) -> None:
        to_remove = []
        for consumable in consumables:
            if player.player_rect.colliderect(consumable.rect):
                consumable.on_consume(player, effect_manager)
                to_remove.append(consumable)

        for item in to_remove:
            consumables.remove(item)
