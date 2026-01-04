import scale_screen as ss


class GameUnit:
    def __init__(self, value: int):
        self.value = value
        self.pixels = ss.game_units_to_px(self.value)


height = GameUnit(12)
