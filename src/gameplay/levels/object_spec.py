from screen.game_units import GameUnit


class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = GameUnit(x).pixels
        self.y = GameUnit(y).pixels
        self.width = GameUnit(width).pixels
        self.height = GameUnit(height).pixels


class SpriteObjectSpec:
    def __init__(self, x: int, y: int, height_units: int, sprite_path: str):
        self.x = GameUnit(x).pixels
        self.y = GameUnit(y).pixels
        self.height = GameUnit(height_units).pixels
        self.sprite_path = sprite_path


class ConsumableSpec(SpriteObjectSpec):
    def __init__(self, *args, kind: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.kind = kind


class DynamicSpriteObjectSpec:
    def __init__(
        self,
        x: int,
        y: int,
        height_units: int,
        segments_count: int,
        sprite_path: str,
        left_sprite_path: str | None = None,
        right_sprite_path: str | None = None,
    ):
        self.x = GameUnit(x).pixels
        self.y = GameUnit(y).pixels
        self.height = GameUnit(height_units).pixels
        self.segments_count = segments_count
        self.sprite_path = sprite_path
        self.left_sprite_path = left_sprite_path
        self.right_sprite_path = right_sprite_path
