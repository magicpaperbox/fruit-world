from typing import Iterator

import pygame

import screen.scale_screen as ss
from gameplay.levels.berry_bush import BerryBush
from gameplay.levels.consumable import Consumable
from gameplay.levels.map.map_spec import MapSpec
from gameplay.levels.map.object_spec import ConsumableSpec, SpriteObjectSpec
from gameplay.levels.npcs import Npc
from render.effects import AnimatedObject, BobbingEffect
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject
from screen.game_units import GameUnit


class Map:
    def __init__(self, spec: MapSpec):
        self.background_img = self._load_map_background(spec.background)
        self.platforms = list(self._load_platforms(spec))
        self.blueberry_bushes = self._load_bushes(list(spec.blueberry_bushes), 1, "blueberry")
        self.strawberry_bushes = self._load_bushes(list(spec.strawberry_bushes), 3, "strawberry")
        self.static_objects = self._load_static_objects(spec.static_objects)
        self.consumable_objects = list(self._load_consumable_objects(spec.consumable))
        self.npcs = []
        for key, value in spec.npcs.items():
            if key == "mouse":
                mouse = Npc.load_mouse(value.x, value.y)
                self.npcs.append(mouse)
        self.neighbours = spec.neighbours

    def _load_platforms(self, spec: MapSpec) -> Iterator[SpriteObject]:
        for platform in spec.old_platforms.values():
            yield SpriteObject.create_invisible(pygame.Rect(platform.x, platform.y, platform.width, platform.height))

        for platform in spec.floating_platforms:
            sprite = SPRITE_FACTORY.load(platform.sprite_path, platform.height)
            yield self._create_sprite_object(platform, sprite)

        for platform in spec.puzzle_platforms:
            current_x = platform.x
            current_y = platform.y

            if platform.left_sprite_path is not None:
                left_sprite = SPRITE_FACTORY.load(platform.left_sprite_path, platform.height)
                yield self._create_sprite_object((current_x, current_y), left_sprite)
                current_x += left_sprite.get_width()

            sprite = SPRITE_FACTORY.load(platform.sprite_path, platform.height)
            width = sprite.get_width()
            for segment in range(platform.segments_count):
                yield self._create_sprite_object((current_x, current_y), sprite)
                current_x += width

            if platform.right_sprite_path is not None:
                right_sprite = SPRITE_FACTORY.load(platform.right_sprite_path, platform.height)
                yield self._create_sprite_object((current_x, current_y), right_sprite)

    def _load_static_objects(self, specs: list[SpriteObjectSpec]):
        static_objects = []
        for obj in specs:
            sprite = SPRITE_FACTORY.load(obj.sprite_path, obj.height)
            sprite_obj = self._create_sprite_object(obj, sprite)
            static_objects.append(sprite_obj)
        return static_objects

    def _load_consumable_objects(self, specs: list[ConsumableSpec]) -> list[Consumable]:
        consumables = []
        for obj_spec in specs:
            sprite = SPRITE_FACTORY.load(obj_spec.sprite_path, obj_spec.height)
            if obj_spec.kind == "heart":
                sprite_obj = AnimatedObject.create(
                    sprite, effects=[BobbingEffect(effect_amplitude=GameUnit(8), speed_factor=0.003)], topleft=(obj_spec.x, obj_spec.y)
                )
            elif obj_spec.kind == "money":
                sprite_obj = AnimatedObject.create(
                    sprite, effects=[BobbingEffect(effect_amplitude=GameUnit(5), speed_factor=0.004)], topleft=(obj_spec.x, obj_spec.y)
                )
            else:
                sprite_obj = self._create_sprite_object(obj_spec, sprite)
            consumable = Consumable(sprite_obj, obj_spec.kind)
            consumables.append(consumable)
        return consumables

    def _load_bushes(self, specs: list[SpriteObjectSpec], count: int, item_id: str):
        bushes = []
        for p in specs:
            sprite = SPRITE_FACTORY.load(p.sprite_path, p.height)
            width = sprite.get_width()
            height = sprite.get_height()
            bushes.append(BerryBush(pygame.Rect(p.x, p.y, width, height), f"sprites/items/{item_id}.png", count, item_id, sprite))

        return bushes

    def _load_map_background(self, sprite_name: str) -> SpriteObject:
        sprite = SPRITE_FACTORY.load_by_width(f"sprites/map/{sprite_name}.png", ss.SCREEN_WIDTH)
        rect = sprite.get_rect(bottom=ss.SCREEN_HEIGHT, centerx=ss.SCREEN_WIDTH // 2)
        return SpriteObject(sprite, rect)

    def _create_sprite_object(self, position, sprite: pygame.Surface):
        if not isinstance(position, tuple):
            position = (position.x, position.y)
        return SpriteObject.create(sprite, topleft=position)


__all__ = ["Map"]
