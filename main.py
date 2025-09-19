import pygame
import sys
from platforms import Platform
from player import Player
from maps_data import load_level, MAP_SPECS
from strawberry import Strawberry

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001

sara = Player.load()
background, platforms = load_level("map1")


player_velocity_y = 0
jumps_left = 2


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


strawberry = Strawberry.load("strawberry", 30, MAP_SPECS["map1"].bushes["krzak 1"].x, MAP_SPECS["map1"].bushes["krzak 1"].y)

running = True
while running:
    dt = clock.tick(FPS)  # ms od poprzedniej klatki

    space_down_this_frame = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            space_down_this_frame = True

    keys = pygame.key.get_pressed()
    is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]
    is_jump_pressed = keys[pygame.K_SPACE]
    is_pick_pressed = keys[pygame.K_1]

    on_ground = False
    prev_x = sara.player_rect.x

    if is_pick_pressed and strawberry is not None:
        if sara.player_rect.colliderect(strawberry.rect):
            strawberry = None


    if is_right_pressed:
        sara.player_rect.x += 2
        facing_dir = "right"
    elif is_left_pressed:
        sara.player_rect.x -= 2
        facing_dir = "left"
    else:
        facing_dir = "front"

    collision_x(platforms, sara.player_rect, prev_x)

    prev_top = sara.player_rect.top
    prev_bottom = sara.player_rect.bottom

    sara.player_rect.y += player_velocity_y * dt  # y
    player_velocity_y += gravity * dt  # dy

    player_velocity_y, on_ground = collision_y(platforms, sara.player_rect, player_velocity_y, prev_top, prev_bottom)

    if space_down_this_frame and jumps_left > 0:
        jumps_left -= 1
        player_velocity_y = -0.4
        on_ground = False
    elif on_ground:
        jumps_left = 2
    sara.update_sprite(facing_dir, on_ground)

    background.draw(screen)
    for p in platforms:
        p.draw(screen)

    # screen.fill((0, 255, 0))
    if strawberry is not None:
        strawberry.draw(screen)
    sara.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
