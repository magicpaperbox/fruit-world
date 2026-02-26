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
        # _anchor is now a list of floats for sub-pixel precision at high FPS
        x, y = GameCoords.from_relative(0.5, 0.5).pixels
        self._anchor = Vector2(x, y)

        self.visual_rect = pygame.Rect((0, 0), GameCoords(60, 115).pixels)
        self.collision_rect_x = pygame.Rect((0, 0), GameCoords(59, 80).pixels)
        self.collision_rect_y = pygame.Rect((0, 0), GameCoords(23, 103).pixels)
        self._max_step_height = 0.25 * self.visual_rect.height

        self._render_offset = GameUnit(15).pixels
        self._belly_offset = GameUnit(-21).pixels
        self._legs_offset = GameUnit(0).pixels

        self.player_velocity_y = 0.0
        self.jumps_left = 2
        self._on_ground = False
        self._horizontal_speed_px_per_s = GameUnit(288).pixels
        self._sync_all_rects()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        # Convert float anchor to int only when setting rect coordinates
        rect.midbottom = int(self._anchor.x), int(self._anchor.y) + y_offset

    def _sync_all_rects(self):
        self._place_rect(self.visual_rect, self._render_offset)
        self._place_rect(self.collision_rect_x, self._belly_offset)
        self._place_rect(self.collision_rect_y, self._legs_offset)

    @property
    def is_on_ground(self) -> bool:
        return self._on_ground

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.visual_rect.x, self.visual_rect.y

    def move_right(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=+1)

    def move_left(self, platforms: list[SpriteObject], dt: int):
        self._move_horizontally(platforms, dt, direction=-1)

    def _move_horizontally(self, platforms: list[SpriteObject], dt: int, direction: int):
        # Apply movement to float anchor
        offset = direction * self._horizontal_speed_px_per_s * (dt / 1000.0)
        self._anchor.x += offset
        self._sync_all_rects()
        x_before_collision = self.collision_rect_x.x
        collision_x(platforms, self.collision_rect_x)

        if self.collision_rect_x.x != x_before_collision:
            step_up = False
            ax, ay = self.collision_rect_x.midbottom
            self._anchor.x = ax
            old_anchor = self._anchor.copy()
            if self._on_ground:
                self._anchor.y -= self._max_step_height
                self._sync_all_rects()
                x_before_collision = self.collision_rect_x.x
                collision_x(platforms, self.collision_rect_x)
                if self.collision_rect_x.x == x_before_collision:
                    _, stepped_on_ground = collision_y(platforms, self.collision_rect_y, 1.0)
                    if stepped_on_ground:
                        step_up = True
                        # self._sync_all_rects()
            if not step_up:
                self._anchor = old_anchor
                self._sync_all_rects()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        # Apply gravity and velocity to float anchor
        self._anchor.y += self.player_velocity_y * dt
        self.player_velocity_y += self._gravity * dt
        self._sync_all_rects()
        y_before_collision = self.collision_rect_y.y
        player_velocity_y, on_ground = collision_y(platforms, self.collision_rect_y, self.player_velocity_y)
        self.player_velocity_y = player_velocity_y
        self._on_ground = on_ground
        if self.collision_rect_y.y != y_before_collision:
            ax, ay = self.collision_rect_y.midbottom
            self._anchor.y = float(ay - self._legs_offset)
            self._sync_all_rects()
        if self._on_ground:
            self.jumps_left = 2

    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = DecimalGameUnit(-0.5).pixels
            self._on_ground = False

    def set_x_position(self, x: int) -> None:
        self._anchor.x = float(x) + self.collision_rect_x.width / 2
        self._sync_all_rects()

    def draw_debug(self, screen: pygame.Surface):
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_x, (250, 250, 0), "X")
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_y, (250, 165, 20), "Y")
