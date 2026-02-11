import screen.scale_screen as ss


class GameUnit:
    def __init__(self, value: int):
        self.value = value
        self.pixels = ss.game_units_to_px(self.value)

    @property
    def non_zero_pixels(self):
        return max(1, self.pixels)


class RelativeUnit:
    def __init__(self, value: float):
        self.value = value
        self.pixels_y = ss.relative_y_to_game_units_px(self.value)
        self.pixels_x = ss.relative_x_to_game_units_px(self.value)
