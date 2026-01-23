import screen.scale_screen as ss


class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.width = ss.game_units_to_px(width)
        self.height = ss.game_units_to_px(height)


class SpriteObjectSpec:
    def __init__(self, x: int, y: int, height_units: int, sprite_path: str):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.height = ss.game_units_to_px(height_units)
        self.sprite_path = sprite_path


class DynamicSpriteObjectSpec:
    def __init__(self, x: int, y: int, height_units: int, segments_count: int, sprite_path: str,
                 left_sprite_path: str | None = None, right_sprite_path: str | None = None):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.height = ss.game_units_to_px(height_units)
        self.segments_count = segments_count
        self.sprite_path = sprite_path
        self.left_sprite_path = left_sprite_path
        self.right_sprite_path = right_sprite_path