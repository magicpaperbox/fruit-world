import pygame

from gameplay.player.player_health import Health
from render.sprite_object import Collectible


class CollectResources:
    def collect(self, player_rect: pygame.Rect, collectibles: list[Collectible], health: Health):
        to_remove = []
        for collectible in collectibles:
            if player_rect.colliderect(collectible.rect):
                if collectible.kind == "heart":
                    health.health_gain()
                    to_remove.append(collectible)

        for item in to_remove:
            collectibles.remove(item)