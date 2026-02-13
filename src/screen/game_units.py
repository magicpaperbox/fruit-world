from typing import Self

import screen.scale_screen as ss


class GameUnit:
    def __init__(self, value: int):
        self.value = value
        self.pixels = ss.game_units_to_px(self.value)

    @property
    def non_zero_pixels(self):
        return max(1, self.pixels)

    @classmethod
    def from_relative_width(cls, width_frac: float) -> Self:
        pass

    @classmethod
    def from_relative_height(cls, height_frac: float) -> Self:
        pass

    @classmethod
    def from_pixels(cls, pixels: int) -> Self:
        pass


GameUnit.from_relative_width(0.03)


class RelativeUnit:
    def __init__(self, value: float):
        self.value = value
        self.pixels_y = ss.relative_y_to_game_units_px(self.value)
        self.pixels_x = ss.relative_x_to_game_units_px(self.value)
