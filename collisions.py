import pygame

from platforms import Platform



def collision_x(solids: list[Platform], player_rect):
    for s in solids:
        if player_rect.colliderect(s.rect):
            distance_from_right_platform = abs(player_rect.left - s.rect.right)
            distance_from_left_platform = abs(player_rect.right - s.rect.left)

            if distance_from_left_platform < distance_from_right_platform:
                player_rect.right = s.rect.left
            else:
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
            distance_from_top_platform = abs(player_rect.top - s.rect.bottom)
            distance_from_bottom_platform = abs(player_rect.bottom - s.rect.top)
            if player_velocity_y > 0 and distance_from_bottom_platform < distance_from_top_platform:
                # spadła na platformę
                player_rect.bottom = s.rect.top
                player_velocity_y = 0
                on_ground = True
            elif player_velocity_y < 0 and distance_from_top_platform < distance_from_bottom_platform:
                # uderzyła w sufit
                player_rect.top = s.rect.bottom
                player_velocity_y = 0
        elif player_rect.bottom == s.rect.top:
            on_ground = True
    return player_velocity_y, on_ground