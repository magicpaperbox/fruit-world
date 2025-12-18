import pygame

from render.sprite_object import SpriteObject


def pick_item(items: list[SpriteObject], player_rect: pygame.Rect, is_pick_pressed: bool) -> int:
    if not is_pick_pressed:
        return 0
    for item in items[:]:  # kopia, bo modyfikujemy listę
        if item.rect.colliderect(player_rect):
            pygame.mixer.Sound("sounds/npc_soft_cue.wav").play()
            items.remove(item)
            return 1
    return 0
