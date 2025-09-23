import pygame

from platforms import Platform


def collision_x(solids: list[Platform], player_rect, prev_x):
    for s in solids:
        if player_rect.colliderect(s.rect):
            if player_rect.x > prev_x:  # kolizja z prawej
                player_rect.right = s.rect.left
            elif player_rect.x < prev_x:  # kolizja z lewej
                player_rect.left = s.rect.right


def collision_y(
        solids: list[Platform],
        player_rect: pygame.Rect,
        player_velocity_y: float,
        prev_top: int,
        prev_bottom: int
) -> tuple[float, bool]:
    on_ground = False
    for s in solids:
        if player_rect.colliderect(s.rect):
            if player_velocity_y > 0 and prev_bottom <= s.rect.top:
                # spadła na platformę
                player_rect.bottom = s.rect.top
                player_velocity_y = 0
                on_ground = True
            elif player_velocity_y < 0 and prev_top >= s.rect.bottom:
                # uderzyła w sufit
                player_rect.top = s.rect.bottom
                player_velocity_y = 0
        elif player_rect.bottom == s.rect.top:
            on_ground = True
    return player_velocity_y, on_ground