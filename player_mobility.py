import pygame
from collisions import collision_x, collision_y
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600



class MovePlayer:
    def __init__(self, gravity: float):
        self._gravity = gravity
        self.player_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, 80)

    def x(self):
        return self.player_rect.x

    def y(self):
        return self.player_rect.y

    def right(self):
        self.player_rect.x += 2

    def left(self):
        self.player_rect.x -= 2

    def check_collision_in_x(self, platforms, prev_x):
        collision_x(platforms, self.player_rect, prev_x)

    def check_collision_in_y(self, platforms, dt, player_velocity_y, prev_top, prev_bottom):
        self.player_rect.y += player_velocity_y * dt  # y
        player_velocity_y += self._gravity * dt  # dy
        player_velocity_y, on_ground = collision_y(platforms, self.player_rect, player_velocity_y, prev_top, prev_bottom)
        return player_velocity_y, on_ground

    @staticmethod
    def jump(space_down_this_frame, jumps_left, on_ground, player_velocity_y):
        if space_down_this_frame and jumps_left > 0:
            jumps_left -= 1
            player_velocity_y = -0.4
            on_ground = False
        elif on_ground:
            jumps_left = 2
        return jumps_left, on_ground, player_velocity_y
