import pygame

from gameplay.player.collisions import collision_x, collision_y
from render.debug import DEBUG_RENDERER
from render.debuggable import Debuggable
from render.sprite_object import SpriteObject
from screen import scale_screen as ss
from screen.game_units import RelativeCoords, RelativeUnit


class PlayerMobility(Debuggable):
    def __init__(self, gravity: float):
        self._gravity = gravity
        # _anchor is now a list of floats for sub-pixel precision at high FPS
        x, y = RelativeCoords(0.5, 0.5).values
        self._anchor: list[float] = [float(x), float(y)]

        self.visual_rect = pygame.Rect((0, 0), RelativeCoords(0.033, 0.1).values)
        self.collision_rect_x = pygame.Rect((0, 0), RelativeCoords(0.032, 0.07).values)
        self.collision_rect_y = pygame.Rect((0, 0), RelativeCoords(0.013, 0.09).values)
        self._max_step_height = 0.25 * self.visual_rect.height

        self._render_offset = 8
        self._belly_offset = -RelativeUnit(0.02).pixels_y
        self._legs_offset = 0

        self.player_velocity_y = 0.0
        self.jumps_left = 2
        self._on_ground = False
        self._horizontal_speed_px_per_s = RelativeUnit(0.15).pixels_x
        self._sync_all_rects()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        ax, ay = self._anchor
        # Convert float anchor to int only when setting rect coordinates
        rect.midbottom = int(ax), int(ay + y_offset)

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
        self._anchor[0] += offset
        self._sync_all_rects()
        x_before_collision = self.collision_rect_x.x
        collision_x(platforms, self.collision_rect_x)

        if self.collision_rect_x.x != x_before_collision:
            step_up = False
            ax, ay = self.collision_rect_x.midbottom
            self._anchor[0] = float(ax)
            old_anchor = self._anchor[0], self._anchor[1]
            if self._on_ground:
                self._anchor[1] -= self._max_step_height
                self._sync_all_rects()
                x_before_collision = self.collision_rect_x.x
                collision_x(platforms, self.collision_rect_x)
                if self.collision_rect_x.x == x_before_collision:
                    _, stepped_on_ground = collision_y(platforms, self.collision_rect_y, 1.0)
                    if stepped_on_ground:
                        step_up = True
                        self._sync_all_rects()
            if not step_up:
                self._anchor[0], self._anchor[1] = old_anchor
                self._sync_all_rects()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        # Apply gravity and velocity to float anchor
        self._anchor[1] += self.player_velocity_y * dt
        self.player_velocity_y += self._gravity * dt
        self._sync_all_rects()
        y_before_collision = self.collision_rect_y.y
        player_velocity_y, on_ground = collision_y(platforms, self.collision_rect_y, self.player_velocity_y)
        self.player_velocity_y = player_velocity_y
        self._on_ground = on_ground
        if self.collision_rect_y.y != y_before_collision:
            ax, ay = self.collision_rect_y.midbottom
            self._anchor[1] = float(ay - self._legs_offset)
            self._sync_all_rects()
        if self._on_ground:
            self.jumps_left = 2

    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = ss.game_units_to_decimal(-0.5)
            self._on_ground = False

    def set_x_position(self, x: int) -> None:
        self._anchor[0] = float(x) + self.collision_rect_x.width / 2
        self._sync_all_rects()

    def draw_debug(self, screen: pygame.Surface):
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_x, (250, 250, 0), "X")
        DEBUG_RENDERER.draw_rect(screen, self.collision_rect_y, (250, 165, 20), "Y")
