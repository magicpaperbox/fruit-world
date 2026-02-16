from gameplay.levels.direction import Direction
from gameplay.levels.object_spec import (
    ConsumableSpec,
    DynamicSpriteObjectSpec,
    ObjectSpec,
    SpriteObjectSpec,
)


class MapSpec:
    def __init__(
        self,
        map_id: str,
        background: str,
        hazard: list[SpriteObjectSpec],
        floating_platforms: list[SpriteObjectSpec],
        puzzle_platforms: list[DynamicSpriteObjectSpec],
        old_platforms: dict[str, ObjectSpec],
        strawberry_bushes: list[SpriteObjectSpec],
        blueberry_bushes: list[SpriteObjectSpec],
        npcs: dict[str, ObjectSpec],
        static_objects: list[SpriteObjectSpec],
        consumable: list[ConsumableSpec],
        neighbours: dict[Direction, str],
    ):
        self.map_id = map_id
        self.background = background
        self.hazard = hazard
        self.floating_platforms = floating_platforms
        self.puzzle_platforms = puzzle_platforms
        self.old_platforms = old_platforms
        self.strawberry_bushes = strawberry_bushes
        self.blueberry_bushes = blueberry_bushes
        self.npcs = npcs
        self.static_objects = static_objects
        self.consumable = consumable
        self.neighbours = neighbours
