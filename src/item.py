import pygame

from render.sprite_object import SpriteObject


def pick_item(items: list[SpriteObject], player_rect: pygame.Rect, is_pick_pressed: bool, remaining_by_key=None) -> int:
    if not is_pick_pressed:
        return 0

    picked = 0
    for item in items[:]:  # kopia, bo modyfikujemy listę
        if player_rect.colliderect(item.rect):
            pygame.mixer.Sound("sounds/npc_soft_cue.wav").play()
            items.remove(item)
            picked += 1

            if remaining_by_key is not None and hasattr(item, "bush_key"):
                k = item.bush_key
                remaining_by_key[k] = max(0, remaining_by_key.get(k, 0) - 1) #odejmujemmy jeden zebrany owoc

            return picked
