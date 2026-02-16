import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.player.player import Player


class ManaPotion(Consumable):
    def on_consume(self, player: Player):
        player.mana.gain()
        pygame.mixer.Sound("sounds/potion_drink.wav").play()
