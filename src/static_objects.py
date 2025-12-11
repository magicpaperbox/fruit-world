from typing import Self
from sprite import SpriteObject


class StaticObject(SpriteObject):
    @classmethod
    def load(cls, sprite_name: str, target_height: int, x: int, y: int) -> Self:
        sprite_path = f"sprites/objects/{sprite_name}.png"
        return super().load(sprite_path, target_height, x, y)
