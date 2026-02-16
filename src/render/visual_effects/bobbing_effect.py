from math import sin

from render.sprite_object import SpriteObject
from render.visual_effect import VisualEffect
from screen.game_units import GameUnit


class BobbingEffect(VisualEffect):
    def __init__(self, effect_amplitude: GameUnit, speed_factor: float):
        self._base_y = None
        self._effect_amplitude = effect_amplitude
        self._speed = speed_factor
        self._now_ms = 0

    def start(self, obj: SpriteObject) -> None:
        self._base_y = obj.rect.y

    def update(self, obj: SpriteObject, dt: int) -> None:
        assert self._base_y is not None
        self._now_ms += dt
        offset_y = int(round(sin(self._now_ms * self._speed) * self._effect_amplitude.pixels))
        obj.rect.y = self._base_y + offset_y
