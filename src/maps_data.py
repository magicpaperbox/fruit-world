import pygame

from map_loading import Map
from bushes import Bush
from npcs import Npc
import src.scale_screen as ss
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject

class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.width = ss.game_units_to_px(width)
        self.height = ss.game_units_to_px(height)


class MapSpec:
    def __init__(
        self,
        background: str,
        platforms: dict[str, ObjectSpec],
        strawberry_bushes: dict[str, ObjectSpec],
        blueberry_bushes: dict[str, ObjectSpec],
        npcs: dict[str, ObjectSpec],
        static_objects: dict[str, ObjectSpec],
    ):
        self.background = background
        self.platforms = platforms
        self.strawberry_bushes = strawberry_bushes
        self.blueberry_bushes = blueberry_bushes
        self.npcs = npcs
        self.static_objects = static_objects

class LoadLevel:
    def __init__(self):
        self.current_screen = None
        self.background_img = None
        self.platforms = []
        self.strawberry_bushes = []
        self.blueberry_bushes = []
        self.npcs = []
        self.static_objects = []


    def load_level(self, map_id: str):
        self.current_screen = MAP_SPECS[map_id]
        self.background_img = Map.load(self.current_screen.background)
        self.platforms = [SpriteObject.create_invisible(pygame.Rect(p.x, p.y, p.width, p.height)) for p in self.current_screen.platforms.values()]
        self.strawberry_bushes = [Bush(p.x, p.y, p.width, p.height) for p in self.current_screen.strawberry_bushes.values()]
        self.blueberry_bushes = [Bush(p.x, p.y, p.width, p.height) for p in self.current_screen.blueberry_bushes.values()]
        self.npcs = []
        for key, value in MAP_SPECS[map_id].npcs.items():
            if key == "mouse":
                self.npcs.append(Npc.load_mouse(value.x, value.y))

        self.static_objects = []
        for key, value in self.current_screen.static_objects.items():
            sprite = SPRITE_FACTORY.load(f"sprites/objects/{key}.png", value.height)
            sprite_obj = SpriteObject.create(sprite, topleft=(value.x, value.y))
            self.static_objects.append(sprite_obj)



MAP_SPECS: dict[str, MapSpec] = {
    "map1": MapSpec(
        background="background_1",
        platforms={
            "lewy gorny krzak": ObjectSpec(300, 430, 350, 98),
            "prawy dolny krzak": ObjectSpec(872, 604, 385, 95),
            "maly gorny krzak": ObjectSpec(630, 128, 226, 90),
            "lewa dolna": ObjectSpec(-38, 799, 740, 101),
            "prawa dolna": ObjectSpec(1200, 799, 285, 101),
            "srodkowa dolna": ObjectSpec(0, 912, 1520, 98),
        },
        strawberry_bushes={
            "krzak 1": ObjectSpec(365, 343, 220, 82),
            "krzak 2": ObjectSpec(970, 500, 228, 98),
            "krzak 3": ObjectSpec(165, 711, 209, 82),
        },
        blueberry_bushes={"krzak 4": ObjectSpec(1270, 706, 137, 88)},
        npcs={"mouse": ObjectSpec(1100, 905, 389, 251)},
        static_objects={"domek": ObjectSpec(970, 676, 389, 251)},
    ),
    "map2": MapSpec(
        background="background_2",
        platforms={
            "lewy gorny krzak": ObjectSpec(300, 430, 350, 98),
            "prawy dolny krzak": ObjectSpec(872, 604, 385, 95),
            "maly gorny krzak": ObjectSpec(630, 128, 226, 90),
            "lewa dolna": ObjectSpec(-38, 799, 740, 101),
            "prawa dolna": ObjectSpec(1200, 799, 285, 101),
            "srodkowa dolna": ObjectSpec(0, 912, 1520, 98),
        },
        strawberry_bushes={},
        blueberry_bushes={},
        npcs={},
        static_objects={},
    ),
}
