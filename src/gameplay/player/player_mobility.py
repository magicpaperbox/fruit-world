import pygame
from pygame import Vector2

from gameplay.player.collisions import collision_x, collision_y
from render.debug import DEBUG_RENDERER
from render.debuggable import Debuggable
from render.sprite_object import SpriteObject
from screen.game_units import DecimalGameUnit, GameCoords, GameUnit


class PlayerMobility(Debuggable):
    def __init__(self, gravity: DecimalGameUnit):
        self._gravity = gravity
        x, y = GameCoords.from_relative(0.5, 0.5).pixels
        self._focal_point = Vector2(x, y)

        self.render_rect = pygame.Rect((0, 0), GameCoords(60, 115).pixels)
        self.collision_rect_x = pygame.Rect((0, 0), GameCoords(59, 80).pixels)
        self.collision_rect_y = pygame.Rect((0, 0), GameCoords(23, 103).pixels)
        self._render_rect_offset = GameUnit(15).pixels
        self._collision_rect_x_offset = GameUnit(-21).pixels
        self._collision_rect_y_offset = GameUnit(0).pixels

        self.jumps_available = 2
        self._is_on_ground = False

        self._velocity_y_px_per_sec = 0
        self._velocity_x_px_per_sec = GameUnit(288).pixels

        self._sync_player_rects()

    @property
    def is_on_ground(self) -> bool:
        return self._is_on_ground

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.render_rect.x, self.render_rect.y

    def jump(self):
        if self.jumps_available > 0:
            self.jumps_available -= 1
            self._velocity_y_px_per_sec = DecimalGameUnit(-500).pixels
            self._is_on_ground = False

    def set_x_position(self, left_x: int) -> None:
        self._focal_point.x = left_x + self.collision_rect_x.width / 2
        self._sync_player_rects()

    def set_y_position(self, bottom_y: int) -> None:
        self._focal_point.y = float(bottom_y - self._collision_rect_y_offset)
        self._sync_player_rects()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        def move_with_velocity():
            dy = self._velocity_y_px_per_sec * (dt / 1000.0)
            self._move_focal_point(dy=dy)

            self._velocity_y_px_per_sec += self._gravity.pixels * (dt / 1000.0)

        def evaluate_collision():
            y_before_collision = self.collision_rect_y.y
            y_after_collision, self._velocity_y_px_per_sec, self._is_on_ground = collision_y(
                platforms, self.collision_rect_y, self._velocity_y_px_per_sec
            )

            if y_before_collision != y_after_collision:
                self.set_y_position(y_after_collision + self.collision_rect_y.height)

        def reset_jumps():
            if self._is_on_ground:
                self.jumps_available = 2

        move_with_velocity()
        evaluate_collision()
        reset_jumps()

    def move_right(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=+1)

    def move_left(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=-1)

    def _move_horizontally(self, platforms: list[SpriteObject], dt: int, direction: int):
        def move_with_velocity():
            dx = direction * self._velocity_x_px_per_sec * (dt / 1000.0)
            self._move_focal_point(dx=dx)

        def evaluate_collision():
            x_before_collision = self.collision_rect_x.x
            x_after_collision = collision_x(platforms, self.collision_rect_x)

            if x_before_collision != x_after_collision:
                self.set_x_position(x_after_collision)

        move_with_velocity()
        evaluate_collision()

    def _move_focal_point(self, *, dx: float = 0.0, dy: float = 0.0):
        self._focal_point.x += dx
        self._focal_point.y += dy
        self._sync_player_rects()

    def _sync_player_rects(self):
        def place_rect(rect: pygame.Rect, y_offset: int):
            rect.midbottom = int(self._focal_point.x), int(self._focal_point.y + y_offset)

        place_rect(self.render_rect, self._render_rect_offset)
        place_rect(self.collision_rect_x, self._collision_rect_x_offset)
        place_rect(self.collision_rect_y, self._collision_rect_y_offset)

    def draw_debug(self, screen: pygame.Surface):
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_x, (250, 250, 0), "X")
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_y, (250, 165, 20), "Y")
