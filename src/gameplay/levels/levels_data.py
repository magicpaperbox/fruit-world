from gameplay.levels.direction import Direction
from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map_spec import MapSpec
from gameplay.levels.object_spec import (
    ConsumableSpec,
    DynamicSpriteObjectSpec,
    ObjectSpec,
    SpriteObjectSpec,
)

LEVEL_1_SPEC = LevelSpec(
    maps=[
        MapSpec(
            map_id="map1",
            background="background",
            hazard=[],
            old_platforms={
                "start": ObjectSpec(x=-5, y=0, width=5, height=1000),
            },
            floating_platforms=[
                SpriteObjectSpec(x=300, y=530, height_units=98, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=872, y=700, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=630, y=228, height_units=90, sprite_path="sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(x=660, y=999, height_units=89, segments_count=2, sprite_path="sprites/objects/dirt_center.png"),
                DynamicSpriteObjectSpec(
                    x=0,
                    y=909,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    right_sprite_path="sprites/objects/grass_ground_right.png",
                ),
                DynamicSpriteObjectSpec(
                    x=1210,
                    y=909,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    left_sprite_path="sprites/objects/grass_ground_left.png",
                ),
            ],
            strawberry_bushes=[
                SpriteObjectSpec(x=365, y=416, height_units=120, sprite_path="sprites/objects/bush_big.png"),
                SpriteObjectSpec(x=970, y=587, height_units=120, sprite_path="sprites/objects/bush_small.png"),
                SpriteObjectSpec(x=165, y=790, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[SpriteObjectSpec(x=970, y=885, height_units=120, sprite_path="sprites/objects/bush_big.png")],
            npcs={"mouse": ObjectSpec(x=1255, y=920, width=389, height=251)},
            static_objects=[SpriteObjectSpec(x=1230, y=695, height_units=251, sprite_path="sprites/objects/domek.png")],
            consumable=[ConsumableSpec(x=500, y=830, kind="mana")],
            neighbours={Direction.RIGHT: "map2"},
        ),
        MapSpec(
            map_id="map2",
            background="background",
            hazard=[
                SpriteObjectSpec(x=950, y=1035, height_units=120, sprite_path="sprites/objects/thorns_narrow.png"),
            ],
            floating_platforms=[
                SpriteObjectSpec(x=1268, y=360, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=298, y=330, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=1080, y=600, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=450, y=665, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=725, y=474, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=755, y=1005, height_units=89, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=1140, y=1005, height_units=89, sprite_path="sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(
                    x=-130,
                    y=909,
                    height_units=175,
                    segments_count=3,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    right_sprite_path="sprites/objects/grass_ground_right.png",
                ),
                DynamicSpriteObjectSpec(
                    x=1300,
                    y=909,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    left_sprite_path="sprites/objects/grass_ground_left.png",
                ),
            ],
            old_platforms={},
            strawberry_bushes=[
                SpriteObjectSpec(x=770, y=360, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
                SpriteObjectSpec(x=245, y=790, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[SpriteObjectSpec(x=1370, y=790, height_units=120, sprite_path="sprites/objects/bush_small.png")],
            npcs={},
            static_objects=[
                SpriteObjectSpec(x=1390, y=250, height_units=118, sprite_path="sprites/objects/yellow_herb.png"),
            ],
            consumable=[
                ConsumableSpec(x=1350, y=290, kind="heart"),
                ConsumableSpec(x=1050, y=810, kind="money"),
            ],
            neighbours={Direction.LEFT: "map1", Direction.RIGHT: "map3"},
        ),
        MapSpec(
            map_id="map3",
            background="background",
            hazard=[],
            floating_platforms=[
                SpriteObjectSpec(x=750, y=800, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=750, y=850, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(
                    x=-130,
                    y=909,
                    height_units=175,
                    segments_count=8,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    right_sprite_path="sprites/objects/grass_ground_right.png",
                ),
            ],
            old_platforms={},
            strawberry_bushes=[
                SpriteObjectSpec(x=525, y=790, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[SpriteObjectSpec(x=1050, y=790, height_units=120, sprite_path="sprites/objects/bush_small.png")],
            npcs={},
            static_objects=[],
            consumable=[],
            neighbours={Direction.LEFT: "map2"},
        ),
    ],
    initial_map_id="map1",
    music_path="sounds/music/Tiny Steps, Big World.mp3",
)
