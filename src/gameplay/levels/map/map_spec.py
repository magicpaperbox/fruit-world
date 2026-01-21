from gameplay.levels.map.direction import Direction
from gameplay.levels.map.object_spec import ObjectSpec, SpriteObjectSpec


class MapSpec:
    def __init__(
        self,
        map_id: str,
        background: str,
        platforms: list[SpriteObjectSpec],
        old_platforms: dict[str, ObjectSpec],
        strawberry_bushes: list[SpriteObjectSpec],
        blueberry_bushes: list[SpriteObjectSpec],
        npcs: dict[str, ObjectSpec],
        static_objects: list[SpriteObjectSpec],
        neighbours: dict[Direction, str],
    ):
        self.map_id = map_id
        self.background = background
        self.platforms = platforms
        self.old_platforms = old_platforms
        self.strawberry_bushes = strawberry_bushes
        self.blueberry_bushes = blueberry_bushes
        self.npcs = npcs
        self.static_objects = static_objects
        self.neighbours = neighbours
