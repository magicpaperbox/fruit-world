import pygame
import random
import scale_screen as ss
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject


class Bush:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 0))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surface, self.rect)

def bush_key(map_id: str, berry_id: str, b: Bush) -> str:
    return f"{map_id}:{berry_id}:{int(b.x)},{int(b.y)},{int(b.width)},{int(b.height)}"


def spawn_berries_for_bushes(
    map_id: str,
    berry_id: str,
    bushes: list[Bush],
    per_bush: int,
    sprite_path: str,
    remaining_by_key: dict[str, int],
    height_px: int = ss.game_units_to_px(42),
):
    sprite = SPRITE_FACTORY.load(sprite_path, height_px)
    jitter_px = ss.game_units_to_px(36)
    rnd = random.Random()
    berries: list[SpriteObject] = []
    if per_bush <= 0:
        return berries

    for b in bushes:
        key = bush_key(map_id, berry_id, b)
        remaining_by_key.setdefault(key, per_bush)
        remaining = remaining_by_key[key]
        if remaining <= 0:
            continue

        x_min = b.x + int(0.1 * b.width)
        x_max = b.x + int(0.9 * b.width)
        y_min = b.y + height_px // 2
        y_max = b.y + b.height - height_px // 2

        slot_w = (x_max - x_min) / max(1, remaining) #nie dzieli przez 0
        jx_max = int(min(jitter_px, int(slot_w * 0.1)))

        for i in range(remaining):
            base_x = x_min + (i + 0.5) * slot_w
            x = base_x + (rnd.randint(-jx_max, jx_max) if jx_max > 0 else 0)
            y = rnd.randint(int(y_min), int(y_max))
            berry = SpriteObject.create(sprite, center=(x, y))

            berry.bush_key = key
            berry.berry_id = berry_id

            berries.append(berry)

    return berries
