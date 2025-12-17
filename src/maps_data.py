from map_loading import Map
from platforms import Platform
from bushes import Bush
from npcs import Npc
import src.scale_screen as ss
from static_objects import StaticObject

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
            "lewy gorny krzak": ObjectSpec(300, 428, 350, 98),
            "prawy dolny krzak": ObjectSpec(872, 602, 385, 95),
            "maly gorny krzak": ObjectSpec(630, 126, 226, 90),
            "lewa dolna": ObjectSpec(-38, 797, 740, 101),
            "prawa dolna": ObjectSpec(1200, 797, 285, 101),
            "srodkowa dolna": ObjectSpec(0, 900, 1520, 98),
        },
        strawberry_bushes={
            "krzak 1": ObjectSpec(365, 343, 220, 82),
            "krzak 2": ObjectSpec(970, 500, 228, 98),
            "krzak 3": ObjectSpec(165, 711, 209, 82),
        },
        blueberry_bushes={"krzak 4": ObjectSpec(1270, 706, 137, 88)},
        npcs={"mouse": ObjectSpec(1100, 907, 389, 251)},
        static_objects={"domek": ObjectSpec(970, 680, 389, 251)},
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
