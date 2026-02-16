import pygame

from gameplay.levels.consumables.consumable import Consumable
from gameplay.player.player import Player


class HealthHeart(Consumable):
    def on_consume(self, player: Player):
        player.health.gain()
        pygame.mixer.Sound("sounds/heart_collect.wav").play()
