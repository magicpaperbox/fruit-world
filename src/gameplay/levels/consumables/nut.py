import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.player.player import Player


class Nut(Consumable):
    def on_consume(self, player: Player):
        player.money.gain()
        pygame.mixer.Sound("sounds/heart_collect.wav").play()
