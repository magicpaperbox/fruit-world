from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map.direction import Direction
from gameplay.levels.map.map_spec import MapSpec
from gameplay.levels.map.object_spec import ObjectSpec, SpriteObjectSpec

LEVEL_1_SPEC = LevelSpec(
    maps=[
        MapSpec(
            map_id="map1",
            background="background",
            old_platforms={
                "start": ObjectSpec(-5, 0, 5, 1000),
                "maly gorny krzak": ObjectSpec(630, 128, 226, 90),
                "lewa dolna": ObjectSpec(-38, 799, 740, 101),
                "prawa dolna": ObjectSpec(1200, 799, 450, 101),
                "srodkowa dolna": ObjectSpec(0, 912, 1520, 98),
            },
            platforms=[
                SpriteObjectSpec(300, 430, 98, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(872, 600, 90, "sprites/objects/platform_wide.png"),
                SpriteObjectSpec(630, 128, 90, "sprites/objects/platform_small.png"),
            ],
            strawberry_bushes={
                "krzak 1": ObjectSpec(365, 343, 220, 82),
                "krzak 2": ObjectSpec(970, 500, 228, 98),
                "krzak 3": ObjectSpec(165, 711, 209, 82),
            },
            blueberry_bushes={"krzak 4": ObjectSpec(1270, 706, 137, 88)},
            npcs={"mouse": ObjectSpec(1100, 905, 389, 251)},
            static_objects=[SpriteObjectSpec(970, 676, 251, "sprites/objects/domek.png")],
            neighbours={Direction.RIGHT: "map2"},
        ),
        MapSpec(
            map_id="map2",
            background="background",
            platforms=[],
            old_platforms={
                "lewy gorny krzak": ObjectSpec(298, 230, 205, 85),
                "srodkowy gorny krzak": ObjectSpec(695, 374, 385, 90),
                "prawy gorny krzak": ObjectSpec(1268, 260, 225, 85),
                "lewy dolny krzak": ObjectSpec(430, 525, 226, 75),
                "prawy dolny krzak": ObjectSpec(1080, 500, 220, 75),
                "lewa dolna": ObjectSpec(0, 799, 790, 201),
                "lewa dolna 2": ObjectSpec(785, 890, 120, 201),
                "prawa dolna": ObjectSpec(1300, 799, 1520, 200),
                "prawa dolna 2": ObjectSpec(1170, 890, 130, 201),
            },
            strawberry_bushes={
                "krzak 1": ObjectSpec(770, 280, 270, 86),
                "krzak 3": ObjectSpec(245, 711, 209, 82),
            },
            blueberry_bushes={"krzak 4": ObjectSpec(1370, 706, 137, 88)},
            npcs={},
            static_objects=[],
            neighbours={Direction.LEFT: "map1"},
        ),
    ],
    initial_map_id="map1",
    music_path="sounds/music/Tiny Steps, Big World.mp3",
)
