import pygame
from gameplay.player.collisions import collision_x, collision_y
from screen import scale_screen as ss
from render.sprite_object import SpriteObject


class PlayerMobility:
    def __init__(self, gravity: float):
        self._gravity = gravity
        self._anchor = ss.relative_coords_to_game_units_px(0.5, 0.5)

        self.visual_rect = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.033, 0.1))
        self.collision_rect_x = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.032, 0.07))
        self.collision_rect_y = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.013, 0.1))

        self._render_offset = 0
        self._belly_offset = -ss.relative_y_to_game_units_px(0.02)
        self._legs_offset = 0

        self.player_velocity_y = 0
        self.jumps_left = 2
        self._on_ground = False
        self._horizontal_speed_px_per_s = ss.relative_x_to_game_units_px(0.15)

        self._sync_all()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        ax, ay = self._anchor
        rect.midbottom = ax, ay + y_offset

    def _sync_all(self):
        self._place_rect(self.visual_rect, self._render_offset)
        self._place_rect(self.collision_rect_x, self._belly_offset)
        self._place_rect(self.collision_rect_y, self._legs_offset)

    def _anchor_from_rect_x_collision(self):
        ax, ay = self.collision_rect_x.midbottom
        return ax, ay - self._belly_offset

    def _anchor_from_rect_y_collision(self):
        ax, ay = self.collision_rect_y.midbottom
        return ax, ay - self._legs_offset

    @property
    def is_on_ground(self):
        return self._on_ground

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.visual_rect.x, self.visual_rect.y

    def move_right(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=+1)

    def move_left(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=-1)

    def _move_horizontally(self, platforms: list[SpriteObject], dt: int, direction: int):
        offset = direction * self._horizontal_speed_px_per_s * (dt / 1000.0)
        self.collision_rect_x.x += offset
        collision_x(platforms, self.collision_rect_x)
        self._anchor = self._anchor_from_rect_x_collision()
        self._sync_all()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        self.collision_rect_y.y += self.player_velocity_y * dt  # y
        self.player_velocity_y += self._gravity * dt  # dy
        player_velocity_y, on_ground = collision_y(platforms, self.collision_rect_y, self.player_velocity_y)
        self.player_velocity_y = player_velocity_y
        self._on_ground = on_ground
        self._anchor = self._anchor_from_rect_y_collision()
        self._sync_all()
        if self._on_ground:
            self.jumps_left = 2

    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = ss.game_units_to_decimal(-0.5)
            self._on_ground = False

    def set_x_position(self, x: int) -> None:
        self.collision_rect_x.x = x
        self._anchor = self._anchor_from_rect_x_collision()
        self._sync_all()
