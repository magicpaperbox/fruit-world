from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map.direction import Direction
from gameplay.levels.map.map_spec import MapSpec
from gameplay.levels.map.object_spec import (
    CollectibleSpec,
    DynamicSpriteObjectSpec,
    ObjectSpec,
    SpriteObjectSpec,
)

LEVEL_1_SPEC = LevelSpec(
    maps=[
        MapSpec(
            map_id="map1",
            background="background",
            old_platforms={
                "start": ObjectSpec(x=-5, y=0, width=5, height=1000),
            },
            floating_platforms=[
                SpriteObjectSpec(x=300, y=430, height_units=98, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=872, y=600, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=630, y=128, height_units=90, sprite_path="sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(
                    x=660, y=889, height_units=89, segments_count=2, sprite_path="sprites/objects/dirt_center.png"
                ),
                DynamicSpriteObjectSpec(
                    x=0,
                    y=799,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    right_sprite_path="sprites/objects/grass_ground_right.png",
                ),
                DynamicSpriteObjectSpec(
                    x=1210,
                    y=799,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    left_sprite_path="sprites/objects/grass_ground_left.png",
                ),
            ],
            strawberry_bushes=[
                SpriteObjectSpec(x=365, y=316, height_units=120, sprite_path="sprites/objects/bush_big.png"),
                SpriteObjectSpec(x=970, y=487, height_units=120, sprite_path="sprites/objects/bush_small.png"),
                SpriteObjectSpec(x=165, y=680, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[
                SpriteObjectSpec(x=1270, y=680, height_units=120, sprite_path="sprites/objects/bush_big.png")
            ],
            npcs={"mouse": ObjectSpec(x=1100, y=905, width=389, height=251)},
            static_objects=[SpriteObjectSpec(x=970, y=676, height_units=251, sprite_path="sprites/objects/domek.png")],
            collectible=[],
            neighbours={Direction.RIGHT: "map2"},
        ),
        MapSpec(
            map_id="map2",
            background="background",
            floating_platforms=[
                SpriteObjectSpec(x=1268, y=260, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=298, y=230, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=1080, y=500, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=430, y=535, height_units=90, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=725, y=374, height_units=90, sprite_path="sprites/objects/platform_wide.png"),
                SpriteObjectSpec(x=695, y=903, height_units=89, sprite_path="sprites/objects/platform_small.png"),
                SpriteObjectSpec(x=1140, y=903, height_units=89, sprite_path="sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(
                    x=-130,
                    y=799,
                    height_units=175,
                    segments_count=3,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    right_sprite_path="sprites/objects/grass_ground_right.png",
                ),
                DynamicSpriteObjectSpec(
                    x=1300,
                    y=799,
                    height_units=175,
                    segments_count=2,
                    sprite_path="sprites/objects/grass_ground_center.png",
                    left_sprite_path="sprites/objects/grass_ground_left.png",
                ),
            ],
            old_platforms={},
            strawberry_bushes=[
                SpriteObjectSpec(x=770, y=260, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
                SpriteObjectSpec(x=245, y=680, height_units=120, sprite_path="sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[
                SpriteObjectSpec(x=1370, y=680, height_units=120, sprite_path="sprites/objects/bush_small.png")
            ],
            npcs={},
            static_objects=[
                SpriteObjectSpec(x=1390, y=150, height_units=118, sprite_path="sprites/objects/yellow_herb.png"),
            ],
            collectible=[
                CollectibleSpec(
                    x=1350,
                    y=190,
                    height_units=50,
                    sprite_path="sprites/items/heart.png",
                    kind="heart"
                )
            ],
            neighbours={Direction.LEFT: "map1"},
        ),
    ],
    initial_map_id="map1",
    music_path="sounds/music/Tiny Steps, Big World.mp3",
)
