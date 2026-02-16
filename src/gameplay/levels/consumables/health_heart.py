from typing import Self

import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.levels.consumables.nut import EffectManager
from gameplay.levels.object_spec import ConsumableSpec
from gameplay.player.player import Player
from render.animated_object import AnimatedObject
from render.sprite_factory import SPRITE_FACTORY
from render.visual_effects.bobbing_effect import BobbingEffect
from screen.game_units import GameUnit


class HealthHeart(Consumable):
    def on_consume(self, player: Player, effect_manager: EffectManager):
        player.health.gain()
        pygame.mixer.Sound("sounds/heart_collect.wav").play()

    @classmethod
    def from_spec(cls, obj_spec: ConsumableSpec) -> Self:
        height = GameUnit(50)
        sprite_path = "sprites/items/heart.png"
        sprite = SPRITE_FACTORY.load(sprite_path, height.pixels)
        sprite_obj = AnimatedObject.create(
            sprite, effects=[BobbingEffect(effect_amplitude=GameUnit(8), speed_factor=0.003)], topleft=obj_spec.pixel_coords
        )
        return cls(sprite_obj)
