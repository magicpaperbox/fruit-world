import pygame
from typing import Self
from sprite import SpriteObject


class Item(SpriteObject):
    @classmethod
    def load(cls, sprite_name: str, target_height: int, x: int=0, y: int=0) -> Self:
        sprite_path = f"sprites/items/{sprite_name}.png"
        return super().load(sprite_path, target_height, x, y)


def pick_item(items: list[Item], player_rect: pygame.Rect, is_pick_pressed: bool) -> int:
    if not is_pick_pressed:
        return 0
    for item in items[:]:  # kopia, bo modyfikujemy listę
        if item.rect.colliderect(player_rect):
            pygame.mixer.Sound("sounds/npc_soft_cue.wav").play()
            items.remove(item)
            return 1
    return 0
