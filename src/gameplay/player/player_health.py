import pygame


class Health:
    def __init__(self):
        self.health_max_points = 5
        self.health_points = 4
        self.restart_game = False


    def die(self):
        self.health_points = 0
        self.restart_game = True

    def health_gain(self):
        if self.health_points < self.health_max_points:
            self.health_points += 1

    def health_leech(self):
        if self.health_points > 0:
            self.health_points -= 1

        if self.health_points == 0:
            self.die()

    def fatal_fall(self, player_rect: pygame.Rect, screen_height: int):
        if player_rect.y > screen_height:
            self.die()

    def collect_life(self, player_rect: pygame.Rect, heart_rect: pygame.Rect):
        if player_rect.colliderect(heart_rect):
            self.health_gain()