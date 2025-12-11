import pygame
import random
from item import Item
from scale_screen import game_units_to_px


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


def spawn_berries_for_bushes(
    bushes: list,
    per_bush: int,
    sprite: str,
    height_px: int = game_units_to_px(42),
):
    jitter_px = game_units_to_px(36)
    rnd = random.Random()
    berries = []
    if per_bush <= 0:
        return berries

    for b in bushes:
        x_min = b.x + int(0.1 * b.width)
        x_max = b.x + int(0.9 * b.width)
        y_min = b.y + height_px // 2
        y_max = b.y + b.height - height_px // 2

        slot_w = (x_max - x_min) / per_bush
        jx_max = int(min(jitter_px, slot_w * 0.1))

        for i in range(per_bush):
            base_x = x_min + (i + 0.5) * slot_w
            x = base_x + (rnd.randint(-jx_max, jx_max) if jx_max > 0 else 0)
            y = rnd.randint(y_min, y_max)
            berry = Item.load(sprite, height_px)
            berry.rect.center = (x, y)
            berries.append(berry)

    return berries
