import pygame
import random
from strawberry import Strawberry


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
    height_px: int = 30,
    seed: int | None = None,
    jitter_px: int = 20,         # drobny rozrzut, by nie nakładały się idealnie
):
    rnd = random.Random(seed)
    berries = []

    for b in bushes:
        for _ in range(per_bush):
            x_min = b.x + 0.2 * b.width
            x_max = b.x + 0.8 * b.width
            x = rnd.uniform(x_min, x_max) + rnd.randint(-jitter_px, jitter_px)

            y = b.y + 0.9 * b.height + rnd.randint(-jitter_px, jitter_px)
            berries.append(Strawberry.load(sprite, height_px, x, y))

    return berries