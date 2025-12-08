import pygame
import random
from item import Item
import scale_screen

SCREEN_WIDTH, SCREEN_HEIGHT = scale_screen.GAME_WIDTH, scale_screen.GAME_HEIGHT


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
    height_px: int = scale_screen.GAME_HEIGHT * 0.04,
    jitter_px: int = 20,  # drobny rozrzut, by nie nakładały się idealnie
):
    rnd = random.Random()
    berries = []
    if per_bush <= 0:
        return berries

    for b in bushes:
        x_min = b.x + 0.1 * b.width
        x_max = b.x + 0.9 * b.width
        y_min = b.y + height_px / 2
        y_max = b.y + b.height - height_px / 2

        slot_w = (x_max - x_min) / per_bush
        jx_max = int(min(jitter_px, slot_w * 0.1))

        for i in range(per_bush):
            base_x = x_min + (i + 0.5) * slot_w
            x = base_x + (rnd.randint(-jx_max, jx_max) if jx_max > 0 else 0)
            y = rnd.uniform(y_min, y_max)
            berries.append(Item.load(sprite, height_px, x, y))

    return berries


def draw_bush_debug(screen, font, bushes, color, label_prefix):
    # półprzezroczysta warstwa
    for idx, b in enumerate(bushes, start=1):
        overlay = pygame.Surface((b.width, b.height), pygame.SRCALPHA)
        # np. zielony/niebieski z alfą ~80/255
        r, g, bcol = color
        overlay.fill((r, g, bcol, 80))
        screen.blit(overlay, (b.x, b.y))
        # obrys
        pygame.draw.rect(screen, color, pygame.Rect(b.x, b.y, b.width, b.height), width=2)
        # etykieta
        label = font.render(f"{label_prefix} {idx}", True, color)
        screen.blit(label, (b.x + 4, b.y + 4))
