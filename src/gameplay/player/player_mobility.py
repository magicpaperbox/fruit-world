import pygame
from pygame import Vector2

from gameplay.player.collisions import collision_x, collision_y
from render.debug import DEBUG_RENDERER
from render.debuggable import Debuggable
from render.sprite_object import SpriteObject
from screen.game_units import DecimalGameUnit, GameCoords, GameUnit


class PlayerMobility(Debuggable):
    def __init__(self, gravity: float):
        self._gravity = gravity
        x, y = GameCoords.from_relative(0.5, 0.5).pixels
        self._focal_point = Vector2(x, y)

        self.render_rect = pygame.Rect((0, 0), GameCoords(60, 115).pixels)
        self.collision_rect_x = pygame.Rect((0, 0), GameCoords(59, 80).pixels)
        self.collision_rect_y = pygame.Rect((0, 0), GameCoords(23, 103).pixels)
        self._render_rect_offset = GameUnit(15).pixels
        self._collision_rect_x_offset = GameUnit(-21).pixels
        self._collision_rect_y_offset = GameUnit(0).pixels

        self._max_step_height = 0.25 * self.render_rect.height
        self._player_velocity_y = 0.0
        self.jumps_available = 2
        self._is_on_ground = False
        self._horizontal_speed_px_per_s = GameUnit(288).pixels
        self._sync_player_parts()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        rect.midbottom = int(self._focal_point.x), int(self._focal_point.y + y_offset)

    def _sync_player_parts(self):
        self._place_rect(self.render_rect, self._render_rect_offset)
        self._place_rect(self.collision_rect_x, self._collision_rect_x_offset)
        self._place_rect(self.collision_rect_y, self._collision_rect_y_offset)

    def _move_focal_point(self, dx=0.0, dy=0.0):
        self._focal_point.x += dx
        self._focal_point.y += dy
        self._sync_player_parts()

    @property
    def is_on_ground(self) -> bool:
        return self._is_on_ground

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.render_rect.x, self.render_rect.y

    def move_right(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=+1)

    def move_left(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=-1)

    def _move_horizontally(self, platforms: list[SpriteObject], dt: int, direction: int):
        dx = direction * self._horizontal_speed_px_per_s * (dt / 1000.0)
        self._move_focal_point(dx=dx)
        x_before_collision = self.collision_rect_x.x
        collision_x(platforms, self.collision_rect_x)

        if self.collision_rect_x.x != x_before_collision:
            ax, ay = self.collision_rect_x.midbottom
            self._focal_point.x = ax
            old_focal_point = self._focal_point.copy()

            if self._is_on_ground:
                self._move_focal_point(dy=-self._max_step_height)
                if not self._make_a_step(platforms):
                    self._focal_point = old_focal_point
                    self._sync_player_parts()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        self._move_focal_point(dy=self._player_velocity_y * dt)
        self._player_velocity_y += self._gravity * dt
        y_before_collision = self.collision_rect_y.y
        player_velocity_y, is_on_ground = collision_y(platforms, self.collision_rect_y, self._player_velocity_y)
        self._player_velocity_y = player_velocity_y
        self._is_on_ground = is_on_ground
        if self.collision_rect_y.y != y_before_collision:
            ax, ay = self.collision_rect_y.midbottom
            self.set_y_position(ay)
        if self._is_on_ground:
            self.jumps_available = 2

    def _make_a_step(self, platforms: list[SpriteObject]) -> bool:
        x_before_collision = self.collision_rect_x.x
        collision_x(platforms, self.collision_rect_x)
        if self.collision_rect_x.x == x_before_collision:
            _, stepped_on_ground = collision_y(platforms, self.collision_rect_y, 1.0)
            return stepped_on_ground
        return False

    def jump(self):
        if self.jumps_available > 0:
            self.jumps_available -= 1
            self._player_velocity_y = DecimalGameUnit(-0.5).pixels
            self._is_on_ground = False

    def set_x_position(self, x: int) -> None:
        self._focal_point.x = float(x + self.collision_rect_x.width / 2)
        self._sync_player_parts()

    def set_y_position(self, y: int) -> None:
        self._focal_point.y = float(y - self._collision_rect_y_offset)
        self._sync_player_parts()

    def draw_debug(self, screen: pygame.Surface):
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_x, (250, 250, 0), "X")
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_y, (250, 165, 20), "Y")
