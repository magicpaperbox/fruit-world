import pygame
from collisions import collision_x, collision_y
from platforms import Platform

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600



class PlayerMobility:
    def __init__(self, gravity: float):
        self._gravity = gravity
        self.player_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, 80)
        self.player_velocity_y = 0
        self.jumps_left = 2
        self._on_ground = False

    def is_on_ground(self):
        return self._on_ground

    def get_coordinates(self) -> tuple[int, int]:
        return self.player_rect.x, self.player_rect.y

    def move_right(self, platforms: list[Platform]):
        self._move_horizontally(platforms, offset=2)

    def move_left(self, platforms: list[Platform]):
        self._move_horizontally(platforms, offset=-2)

    def _move_horizontally(self, platforms: list[Platform], offset: int):
        prev_x = self.player_rect.x
        self.player_rect.x += offset
        self._check_collision_in_x(platforms, prev_x)

    def _check_collision_in_x(self, platforms, prev_x):
        collision_x(platforms, self.player_rect, prev_x)

    def move_vertically(self, platforms: list[Platform], dt: int):
        prev_top = self.player_rect.top
        prev_bottom = self.player_rect.bottom
        self.player_rect.y += self.player_velocity_y * dt  # y
        self.player_velocity_y += self._gravity * dt  # dy
        player_velocity_y, on_ground = collision_y(platforms, self.player_rect, self.player_velocity_y, prev_top, prev_bottom)
        self._on_ground = on_ground
        self.player_velocity_y = player_velocity_y
        if self._on_ground:
            self.jumps_left = 2

    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = -0.4
            self._on_ground = False


