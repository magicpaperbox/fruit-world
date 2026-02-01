import pygame

from gameplay.levels.consumable import Consumable
from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana


def collect_consumables(player_rect: pygame.Rect, consumables: list[Consumable], health: Health, mana: Mana):
    to_remove = []
    for consumable in consumables:
        if player_rect.colliderect(consumable.rect):
            if consumable.kind == "heart":
                health.gain()
                pygame.mixer.Sound("sounds/heart_collect.wav").play()
                to_remove.append(consumable)
            if consumable.kind == "mana":
                mana.gain()
                pygame.mixer.Sound("sounds/potion_drink.wav").play()
                to_remove.append(consumable)

    for item in to_remove:
        consumables.remove(item)
