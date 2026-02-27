from typing import Self

import screen.scale_screen as ss


class DecimalGameUnit:
    def __init__(self, value: float):
        self.value = value
        self.pixels = ss.game_units_to_decimal_px(self.value)

    @classmethod
    def from_relative_width(cls, width_frac: float) -> Self:
        return cls(ss.canonical_game_width() * width_frac)

    @classmethod
    def from_relative_height(cls, height_frac: float) -> Self:
        return cls(ss.canonical_game_height() * height_frac)


class GameUnit:
    def __init__(self, value: int):
        self.value = value
        self.pixels = ss.game_units_to_px(self.value)

    @property
    def non_zero_pixels(self):
        return max(1, self.pixels)

    @classmethod
    def from_relative_width(cls, width_frac: float) -> Self:
        return cls(int(ss.canonical_game_width() * width_frac))

    @classmethod
    def from_relative_height(cls, height_frac: float) -> Self:
        return cls(int(ss.canonical_game_height() * height_frac))

    @classmethod
    def from_pixels(cls, pixels: int) -> Self:
        raise NotImplementedError


class GameCoords:
    def __init__(self, x_value: int, y_value: int):
        self.x = GameUnit(x_value)
        self.y = GameUnit(y_value)

    @property
    def pixels(self) -> tuple[int, int]:
        return self.x.pixels, self.y.pixels

    @classmethod
    def from_relative(cls, width_frac: float, height_frac: float) -> Self:
        return cls(GameUnit.from_relative_width(width_frac).value, GameUnit.from_relative_height(height_frac).value)
