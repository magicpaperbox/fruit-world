import pygame


class Health:
    def __init__(self):
        self.health_max_points = 5
        self.health_points = 2
        self._is_dead = False

    @property
    def is_dead(self) -> bool:
        return self._is_dead

    def die(self):
        self.health_points = 0
        self._is_dead = True

    def gain(self):
        if self.health_points < self.health_max_points:
            self.health_points += 1

    def leech(self):
        if self.health_points > 0:
            self.health_points -= 1

        if self.health_points == 0:
            self.die()

    def fatal_fall(self, player_rect: pygame.Rect, screen_height: int):
        if player_rect.y > screen_height:
            self.die()
