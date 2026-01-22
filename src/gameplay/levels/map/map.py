import pygame

import screen.scale_screen as ss
from gameplay.levels.berry_bush import BerryBush
from gameplay.levels.map.map_spec import MapSpec
from gameplay.levels.map.object_spec import SpriteObjectSpec
from gameplay.levels.npcs import Npc
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject


class Map:
    def __init__(self, spec: MapSpec):
        self.background_img = self._load_map_background(spec.background)
        self.platforms = self._load_platforms(spec)
        self.blueberry_bushes = self._load_bushes(list(spec.blueberry_bushes), 1, "blueberry")
        self.strawberry_bushes = self._load_bushes(list(spec.strawberry_bushes), 3, "strawberry")
        self.static_objects = self._load_static_objects(spec.static_objects)
        self.npcs = []
        for key, value in spec.npcs.items():
            if key == "mouse":
                mouse = Npc.load_mouse(value.x, value.y)
                self.npcs.append(mouse)
        self.neighbours = spec.neighbours

    def _load_platforms(self, spec: MapSpec):
        old_platforms = [
            SpriteObject.create_invisible(pygame.Rect(p.x, p.y, p.width, p.height)) for p in spec.old_platforms.values()
        ]
        new_platforms = []
        for p in spec.floating_platforms:
            sprite = SPRITE_FACTORY.load(p.sprite_path, p.height)
            sprite_obj = SpriteObject.create(sprite, topleft=(p.x, p.y))
            new_platforms.append(sprite_obj)

        for p in spec.puzzle_platforms:
            sprite = SPRITE_FACTORY.load(p.sprite_path, p.height)
            width = sprite.get_width()
            if p.segments_count > 1:

                for segment in range(p.segments_count):
                    sprite_obj = SpriteObject.create(sprite, topleft=(p.x, p.y))
                    new_platforms.append(sprite_obj)
                    p.x = p.x + width
            else:
                sprite_obj = SpriteObject.create(sprite, topleft=(p.x, p.y))
                new_platforms.append(sprite_obj)

        return old_platforms + new_platforms

    def _load_static_objects(self, specs: list[SpriteObjectSpec]):
        static_objects = []
        for obj in specs:
            sprite = SPRITE_FACTORY.load(obj.sprite_path, obj.height)
            sprite_obj = SpriteObject.create(sprite, topleft=(obj.x, obj.y))
            static_objects.append(sprite_obj)
        return static_objects

    def _load_bushes(self, specs: list[SpriteObjectSpec], count: int, item_id: str):
        bushes = []
        for p in specs:
            sprite = SPRITE_FACTORY.load(p.sprite_path, p.height)
            width = sprite.get_width()
            height = sprite.get_height()
            bushes.append(BerryBush(pygame.Rect(p.x, p.y, width, height), f"sprites/items/{item_id}.png", count, item_id, sprite))

        return bushes

    def _load_map_background(self, sprite_name: str) -> SpriteObject:
        sprite = SPRITE_FACTORY.load(f"sprites/map/{sprite_name}.png", ss.GAME_HEIGHT)
        rect = sprite.get_rect(center=ss.relative_coords_to_game_units_px(0.5, 0.5))
        return SpriteObject(sprite, rect)


__all__ = ["Map"]
