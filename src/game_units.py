from scale_screen import game_units_to_px


class GameUnit:
    def __init__(self, value: int):
        self.value = value
        self.pixels = game_units_to_px(self.value)

height = GameUnit(12)