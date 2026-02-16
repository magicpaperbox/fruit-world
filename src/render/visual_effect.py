import abc

from render.sprite_object import SpriteObject


class VisualEffect(abc.ABC):
    def start(self, obj: SpriteObject) -> None:
        pass

    @abc.abstractmethod
    def update(self, obj: SpriteObject, now_ms: int) -> None:
        pass
