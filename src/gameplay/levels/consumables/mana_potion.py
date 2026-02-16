from typing import Self

import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.levels.object_spec import ConsumableSpec
from gameplay.player.player import Player
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject
from screen.game_units import GameUnit


class ManaPotion(Consumable):
    def on_consume(self, player: Player):
        player.mana.gain()
        pygame.mixer.Sound("sounds/potion_drink.wav").play()

    @classmethod
    def from_spec(cls, obj_spec: ConsumableSpec) -> Self:
        height = GameUnit(70)
        sprite_path = "sprites/items/mana_potion.png"
        sprite = SPRITE_FACTORY.load(sprite_path, height.pixels)
        sprite_obj = SpriteObject.create(sprite, topleft=obj_spec.pixel_coords)
        return cls(sprite_obj)
