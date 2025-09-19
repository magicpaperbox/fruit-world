from maps import Map
from platforms import Platform


class PlatformSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class MapSpec:
    def __init__(self, background: str, platforms: dict[str, PlatformSpec]):
        self.background = background
        self.platforms = platforms


def load_level(map_id: str):
    current_screen = MAP_SPECS[map_id]
    background_img = Map.load(current_screen.background)
    platforms = [Platform(p.x, p.y, p.width, p.height) for p in current_screen.platforms.values()]
    return background_img, platforms


MAP_SPECS: dict[str, MapSpec] = {
    "map1": MapSpec(
        background="background_1",
        platforms={
            "lewy gorny krzak": PlatformSpec(165, 260, 193, 60),
            "prawy dolny krzak": PlatformSpec(477, 368, 212, 60),
            "maly gorny krzak": PlatformSpec(346, 78, 119, 55),
            "lewa dolna": PlatformSpec(0, 488, 380, 62),
            "prawa dolna": PlatformSpec(660, 488, 150, 62),
            "srodkowa dolna": PlatformSpec(0, 550, 800, 60)
        })
}
