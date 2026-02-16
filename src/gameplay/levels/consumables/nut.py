from typing import Self

import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.levels.object_spec import ConsumableSpec
from gameplay.player.player import Player
from render.animated_object import AnimatedObject
from render.effect_manager import EffectManager
from render.sprite_factory import SPRITE_FACTORY
from render.visual_effects.bobbing_effect import BobbingEffect
from render.visual_effects.particles_effect import ParticlesEffect
from screen.game_units import GameUnit


class Nut(Consumable):
    def __init__(self, sprite_obj: AnimatedObject):
        super().__init__(sprite_obj)
        self._animated_obj = sprite_obj

    def on_consume(self, player: Player, effect_manager: EffectManager):
        player.money.gain()
        pygame.mixer.Sound("sounds/heart_collect.wav").play()
        effect_manager.add_effect(ParticlesEffect(), self.rect.center)

    @classmethod
    def from_spec(cls, obj_spec: ConsumableSpec) -> Self:
        height = GameUnit(50)
        sprite_path = "sprites/items/nut_money.png"
        sprite = SPRITE_FACTORY.load(sprite_path, height.pixels)
        sprite_obj = AnimatedObject.create(
            sprite, effects=[BobbingEffect(effect_amplitude=GameUnit(5), speed_factor=0.004)], topleft=obj_spec.pixel_coords
        )
        return cls(sprite_obj)
