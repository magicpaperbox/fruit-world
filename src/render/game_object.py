from typing import Protocol


class GameObject(Protocol):
    def update(self, dt: int):
        pass
