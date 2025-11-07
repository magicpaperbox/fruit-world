from map_loading import Map
from platforms import Platform
from bushes import Bush
from npcs import Npc
from static_objects import StaticObject


class PlatformSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = width * height


class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class MapSpec:
    def __init__(
            self,
            background: str,
            platforms: dict[str, PlatformSpec],
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
        static_objects.append(
            StaticObject.load(key, value.height, value.x, value.y)
        )

    return background_img, platforms, strawberry_bushes, blueberry_bushes, npcs, static_objects


MAP_SPECS: dict[str, MapSpec] = {
    "map1": MapSpec(
        background="background_1",
        platforms={
            "lewy gorny krzak": PlatformSpec(165, 262, 193, 60),
            "prawy dolny krzak": PlatformSpec(477, 370, 212, 60),
            "maly gorny krzak": PlatformSpec(346, 78, 119, 55),
            "lewa dolna": PlatformSpec(-20, 490, 380, 62),
            "prawa dolna": PlatformSpec(660, 490, 150, 62),
            "srodkowa dolna": PlatformSpec(0, 555, 800, 60)
        },
        strawberry_bushes={
            "krzak 1": ObjectSpec(200, 210, 120, 50),
            "krzak 2": ObjectSpec(535, 310, 120, 60),
            "krzak 3": ObjectSpec(90, 435, 110, 50)
        },
        blueberry_bushes={
            "krzak 4": ObjectSpec(685, 440, 90, 45)
        },
        npcs={
            "mouse": ObjectSpec(580, 555, 80, 50)
        },
        static_objects={
            "domek": ObjectSpec(610, 495, 200, 140)
        }
    ),
    "map2": MapSpec(
        background="background_2",
        platforms={
            "lewy krzak": PlatformSpec(165, 262, 193, 60),
            "prawy krzak": PlatformSpec(477, 370, 212, 60),
            "maly gorny krzak": PlatformSpec(346, 78, 119, 55),
            "lewa dolna": PlatformSpec(0, 490, 380, 62),
            "prawa dolna": PlatformSpec(660, 490, 150, 62),
            "srodkowa dolna": PlatformSpec(0, 555, 800, 60)
        },
        strawberry_bushes={

        },
        blueberry_bushes={

        },
        npcs={

        },
        static_objects={

        }
    ),
}
