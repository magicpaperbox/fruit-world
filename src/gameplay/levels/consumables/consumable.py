import pygame

from gameplay.player.player import Player
from render.drawable import Drawable
from render.game_object import GameObject
from render.sprite_object import SpriteObject


class Consumable(Drawable, GameObject):
    def __init__(self, sprite_obj: SpriteObject, kind: str):
        self._sprite_obj = sprite_obj
        self.kind = kind

    @property
    def rect(self):
        return self._sprite_obj.rect

    def draw(self, screen: pygame.surface.Surface):
        self._sprite_obj.draw(screen)

    def update(self, now_ms: int) -> None:
        self._sprite_obj.update(now_ms)

    def on_consume(self, player: Player):
        raise NotImplementedError()

    @staticmethod
    def consume(consumables: list["Consumable"], player: Player) -> list[tuple[int, int]]:
        collected_positions = []
        to_remove = []
        for consumable in consumables:
            if player.player_rect.colliderect(consumable.rect):
                consumable.on_consume(player)
                to_remove.append(consumable)
                if consumable.kind == "money":
                    collected_positions.append(consumable.rect.center)

        for item in to_remove:
            consumables.remove(item)

        return collected_positions
