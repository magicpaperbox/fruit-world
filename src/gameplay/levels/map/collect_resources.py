import pygame

from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from render.sprite_object import Collectible


class CollectResources:
    def collect(self, player_rect: pygame.Rect, collectibles: list[Collectible], health: Health, mana: Mana):
        to_remove = []
        for collectible in collectibles:
            if player_rect.colliderect(collectible.rect):
                if collectible.kind == "heart":
                    health.gain()
                    pygame.mixer.Sound("sounds/heart_collect.wav").play()
                    to_remove.append(collectible)
                if collectible.kind == "mana":
                    mana.gain()
                    pygame.mixer.Sound("sounds/potion_drink.wav").play()
                    to_remove.append(collectible)


        for item in to_remove:
            collectibles.remove(item)