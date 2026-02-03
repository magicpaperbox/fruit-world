import pygame

from gameplay.levels.consumable import Consumable
from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from gameplay.player.player_money import Money


def collect_consumables(
    player_rect: pygame.Rect, consumables: list[Consumable], money: Money, health: Health, mana: Mana
) -> list[tuple[int, int]]:
    collected_positions = []
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
            if consumable.kind == "money":
                money.gain()
                pygame.mixer.Sound("sounds/heart_collect.wav").play()
                to_remove.append(consumable)
                collected_positions.append(consumable.rect.center)

    for item in to_remove:
        consumables.remove(item)

    return collected_positions
