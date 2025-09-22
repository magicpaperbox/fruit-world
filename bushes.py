import pygame
from random import Random


class Bush:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 0))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surface, self.rect)




class FruitSpawner:
    def __init__(
        self,
        map_specs,
        map_name: str,
        sprite_name: str,
        fruit_size: int,
        max_total: int = 4,
        max_per_bush: int = 2,
        respawn_ms: int = 6000,
        jitter_px: int = 8,           # lekkie rozrzucenie pozycji na krzaku
        rng_seed: int | None = None,  # ustaw seed dla powtarzalności
    ):
        self.map_specs = map_specs
        self.map_name = map_name
        self.sprite_name = sprite_name
        self.fruit_size = fruit_size
        self.max_total = max_total
        self.max_per_bush = max_per_bush
        self.respawn_ms = respawn_ms
        self.jitter_px = jitter_px
        self.rng = Random(rng_seed)

        self.bushes = self.map_specs[self.map_name].bushes
        self.active: list[tuple[str, Strawberry]] = []  # (nazwa_krzaka, obiekt)
        self.per_bush_counts = defaultdict(int)
        self.respawn_queue: list[tuple[str, int]] = []  # (nazwa_krzaka, timestamp_ready_ms)