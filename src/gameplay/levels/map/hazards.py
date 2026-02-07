import pygame

from gameplay.player.player_health import Health
from render.sprite_object import SpriteObject


class Hazard:
    def __init__(self):
        self._cooldown_timer = 0
        self._cooldown_duration = 2000

    def update(self, dt_ms: int):
        if self._cooldown_timer > 0:
            self._cooldown_timer -= dt_ms

    def collide_hazard(self, hazards: list[SpriteObject], player_rect: pygame.Rect, health: Health):
        for hazard in hazards:
            if player_rect.colliderect(hazard.rect):
                if self._cooldown_timer <= 1:
                    health.leech()
                    self._cooldown_timer = self._cooldown_duration
