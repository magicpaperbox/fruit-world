from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map.direction import Direction
from gameplay.levels.map.map_spec import MapSpec
from gameplay.levels.map.object_spec import ObjectSpec, SpriteObjectSpec, DynamicSpriteObjectSpec

LEVEL_1_SPEC = LevelSpec(
    maps=[
        MapSpec(
            map_id="map1",
            background="background",
            old_platforms={
                "start": ObjectSpec(-5, 0, 5, 1000),
            },
            floating_platforms=[
                SpriteObjectSpec(300, 430, 98, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(872, 600, 90, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(630, 128, 90, "sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(660, 889, 89, 2, "sprites/objects/dirt_center.png"),
                DynamicSpriteObjectSpec(0, 799, 175, 2, "sprites/objects/grass_ground_center.png", None, "sprites/objects/grass_ground_right.png"),
                DynamicSpriteObjectSpec(1270, 799, 175, 2, "sprites/objects/grass_ground_center.png", "sprites/objects/grass_ground_left.png"),
            ],
            strawberry_bushes=[
                SpriteObjectSpec(365, 316, 120, "sprites/objects/bush_big.png"),
                SpriteObjectSpec(970, 487, 120, "sprites/objects/bush_small.png"),
                SpriteObjectSpec(165, 680, 120, "sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[SpriteObjectSpec(1270, 680, 120, "sprites/objects/bush_big.png")],
            npcs={"mouse": ObjectSpec(1100, 905, 389, 251)},
            static_objects=[SpriteObjectSpec(970, 676, 251, "sprites/objects/domek.png")],
            neighbours={Direction.RIGHT: "map2"},
        ),
        MapSpec(
            map_id="map2",
            background="background",
            floating_platforms=[
                SpriteObjectSpec(1268, 260, 90, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(298, 230, 90, "sprites/objects/platform_small.png"),
                SpriteObjectSpec(1080, 500, 90, "sprites/objects/platform_small.png"),
                SpriteObjectSpec(430, 535, 90, "sprites/objects/platform_small.png"),
                SpriteObjectSpec(725, 374, 90, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(695, 903, 89, "sprites/objects/platform_small.png"),
                SpriteObjectSpec(1140, 903, 89, "sprites/objects/platform_small.png"),
            ],
            puzzle_platforms=[
                DynamicSpriteObjectSpec(-130, 799, 175, 3, "sprites/objects/grass_ground_center.png", None, "sprites/objects/grass_ground_right.png"),
                DynamicSpriteObjectSpec(1300, 799, 175, 2, "sprites/objects/grass_ground_center.png", "sprites/objects/grass_ground_left.png"),
            ],
            old_platforms={},
            strawberry_bushes=[
                SpriteObjectSpec(770, 260, 120, "sprites/objects/bush_wide.png"),
                SpriteObjectSpec(245, 680, 120, "sprites/objects/bush_wide.png"),
            ],
            blueberry_bushes=[SpriteObjectSpec(1370, 680, 120, "sprites/objects/bush_small.png")],
            npcs={},
            static_objects=[],
            neighbours={Direction.LEFT: "map1"},
        ),
    ],
    initial_map_id="map1",
    music_path="sounds/music/Tiny Steps, Big World.mp3",
)
