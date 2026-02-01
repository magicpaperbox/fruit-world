from typing import Protocol


class GameObject(Protocol):
    def update(self, now_ms: int):
        pass
