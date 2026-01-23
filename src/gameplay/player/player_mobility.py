import pygame
from gameplay.player.collisions import collision_x, collision_y
from screen import scale_screen as ss
from render.sprite_object import SpriteObject


class PlayerMobility:
    def __init__(self, gravity: float):
        self._gravity = gravity
        # _anchor is now a list of floats for sub-pixel precision at high FPS
        x, y = ss.relative_coords_to_game_units_px(0.5, 0.5)
        self._anchor: list[float] = [float(x), float(y)]

        self.visual_rect = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.033, 0.1))
        self.collision_rect_x = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.032, 0.07))
        self.collision_rect_y = pygame.Rect((0, 0), ss.relative_coords_to_game_units_px(0.013, 0.09))

        self._render_offset = 8
        self._belly_offset = -ss.relative_y_to_game_units_px(0.02)
        self._legs_offset = 0

        self.player_velocity_y = 0.0
        self.jumps_left = 2
        self._on_ground = False
        self._horizontal_speed_px_per_s = ss.relative_x_to_game_units_px(0.15)

        self._sync_all()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        ax, ay = self._anchor
        # Convert float anchor to int only when setting rect coordinates
        rect.midbottom = int(ax), int(ay + y_offset)

    def _sync_all(self):
        self._place_rect(self.visual_rect, self._render_offset)
        self._place_rect(self.collision_rect_x, self._belly_offset)
        self._place_rect(self.collision_rect_y, self._legs_offset)

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
        # Apply movement to float anchor
        offset = direction * self._horizontal_speed_px_per_s * (dt / 1000.0)
        self._anchor[0] += offset
        # Sync rects to check collisions
        self._sync_all()
        # Remember rect position before collision check
        old_x = self.collision_rect_x.x
        # Check collisions - this may move the rect
        collision_x(platforms, self.collision_rect_x)
        # Update anchor from rect ONLY if collision moved it
        if self.collision_rect_x.x != old_x:
            ax, ay = self.collision_rect_x.midbottom
            self._anchor[0] = float(ax)
            self._sync_all()

    def move_vertically(self, platforms: list[SpriteObject], dt: int):
        # Apply gravity and velocity to float anchor
        self._anchor[1] += self.player_velocity_y * dt
        self.player_velocity_y += self._gravity * dt
        # Sync rects to check collisions
        self._sync_all()
        # Remember rect position before collision check
        old_y = self.collision_rect_y.y
        # Check collisions - this may move the rect and update velocity
        player_velocity_y, on_ground = collision_y(platforms, self.collision_rect_y, self.player_velocity_y)
        self.player_velocity_y = player_velocity_y
        self._on_ground = on_ground
        # Update anchor from rect ONLY if collision moved it
        if self.collision_rect_y.y != old_y:
            ax, ay = self.collision_rect_y.midbottom
            self._anchor[1] = float(ay - self._legs_offset)
            self._sync_all()
        if self._on_ground:
            self.jumps_left = 2

    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = ss.game_units_to_decimal(-0.5)
            self._on_ground = False

    def set_x_position(self, x: int) -> None:
        self._anchor[0] = float(x) + self.collision_rect_x.width / 2
        self._sync_all()
