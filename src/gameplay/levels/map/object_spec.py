import screen.scale_screen as ss


class ObjectSpec:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = ss.game_units_to_px(x)
        self.y = ss.game_units_to_px(y)
        self.width = ss.game_units_to_px(width)
        self.height = ss.game_units_to_px(height)
