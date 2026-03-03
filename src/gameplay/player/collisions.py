import pygame

from gameplay.levels.direction import Direction
from render.sprite_object import SpriteObject


def collision_x(solids: list[SpriteObject], player_rect: pygame.Rect) -> int:
    new_left = player_rect.left
    for solid in solids:
        if player_rect.colliderect(solid.rect):
            distance_from_right_platform = abs(player_rect.left - solid.rect.right)
            distance_from_left_platform = abs(player_rect.right - solid.rect.left)

            if distance_from_left_platform < distance_from_right_platform:
                new_left = solid.rect.left - player_rect.width
            else:
                new_left = solid.rect.right
    return new_left


def collision_y(
    solids: list[SpriteObject],
    player_rect: pygame.Rect,
    player_velocity_y: float,
) -> tuple[int, float, bool]:
    on_ground = False
    new_top = player_rect.top
    for solid in solids:
        if player_rect.colliderect(solid.rect):
            distance_from_top_platform = abs(player_rect.top - solid.rect.bottom)
            distance_from_bottom_platform = abs(player_rect.bottom - solid.rect.top)
            if player_velocity_y > 0 and distance_from_bottom_platform < distance_from_top_platform:
                # floor
                # player_rect.bottom = solid.rect.top
                new_top = solid.rect.top - player_rect.height
                player_velocity_y = 0
                on_ground = True
            elif player_velocity_y < 0 and distance_from_top_platform < distance_from_bottom_platform:
                # ceiling
                new_top = solid.rect.bottom
                player_velocity_y = 0
        elif player_rect.bottom == solid.rect.top and player_rect.right > solid.rect.left and player_rect.left < solid.rect.right:
            on_ground = True
    return new_top, player_velocity_y, on_ground


def stairs(
    stairs: list[SpriteObject],
    player_rect: pygame.Rect,
    direction: Direction,
):
    for s in stairs:
        if player_rect.colliderect(s.rect):
            if direction == Direction.UP:
                player_rect.bottom = s.rect.top
            elif direction == Direction.DOWN:
                pass
                # player_rect.bottom = s.rect.top  - tu nie moze byc bottom bo co jak schopek sie konczy pod ziemia
