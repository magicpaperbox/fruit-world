import pygame

class Mana:
    def __init__(self):
        self.mana_max_points = 5
        self.mana_points = 3

    def gain(self):
        if self.mana_points < self.mana_max_points:
            self.mana_points += 1

    def cast_spell(self):
        if self.mana_points > 0:
            self.mana_points -= 1