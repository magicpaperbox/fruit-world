from map_loading import Map
from platforms import Platform
from bushes import Bush
from npcs import Npc
from src.scale_screen import game_units_to_px
from static_objects import StaticObject

class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = game_units_to_px(x)
        self.y = game_units_to_px(y)
        self.width = game_units_to_px(width)
        self.height = game_units_to_px(height)


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


def load_level(map_id: str):
    current_screen = MAP_SPECS[map_id]
    background_img = Map.load(current_screen.background)
    platforms = [Platform(p.x, p.y, p.width, p.height) for p in current_screen.platforms.values()]
    strawberry_bushes = [Bush(p.x, p.y, p.width, p.height) for p in current_screen.strawberry_bushes.values()]
    blueberry_bushes = [Bush(p.x, p.y, p.width, p.height) for p in current_screen.blueberry_bushes.values()]
    npcs = []
    for key, value in MAP_SPECS[map_id].npcs.items():
        if key == "mouse":
            npcs.append(Npc.load_mouse(value.x, value.y))

    static_objects = []
    for key, value in current_screen.static_objects.items():
        static_objects.append(StaticObject.load(key, value.height, value.x, value.y))

    return (
        background_img,
        platforms,
        strawberry_bushes,
        blueberry_bushes,
        npcs,
        static_objects,
    )


MAP_SPECS: dict[str, MapSpec] = {
    "map1": MapSpec(
        background="background_1",
        platforms={
            "lewy gorny krzak": ObjectSpec(314, 428, 367, 98),
            "prawy dolny krzak": ObjectSpec(906, 604, 403, 98),
            "maly gorny krzak": ObjectSpec(657, 127, 226, 90),
            "lewa dolna": ObjectSpec(-38, 800, 760, 101),
            "prawa dolna": ObjectSpec(1254, 800, 285, 101),
            "srodkowa dolna": ObjectSpec(0, 907, 1520, 98),
        },
        strawberry_bushes={
            "krzak 1": ObjectSpec(380, 343, 228, 82),
            "krzak 2": ObjectSpec(1017, 506, 228, 98),
            "krzak 3": ObjectSpec(171, 711, 209, 82),
        },
        blueberry_bushes={"krzak 4": ObjectSpec(1322, 706, 137, 88)},
        npcs={"mouse": ObjectSpec(1125, 907, 389, 251)},
        static_objects={"domek": ObjectSpec(1132, 809, 389, 251)},
    ),
    "map2": MapSpec(
        background="background_2",
        platforms={},
        strawberry_bushes={},
        blueberry_bushes={},
        npcs={},
        static_objects={},
    ),
}
