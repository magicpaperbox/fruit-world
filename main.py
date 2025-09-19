import pygame
import sys
from animation import Animation
from platforms import Platform
from player import Player
from maps_data import load_level

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001

player = Player.load(sprite_name="static")
background, platforms = load_level("map1")
player_img = player.sprite

player_rect = player.player_rect
player_velocity_y = 0
jumps_left = 2

player_left2 = Player.load("left_1").sprite
move_left_animation = Animation(duration=10, frames=Player.move_left())

player_right2 = Player.load("right_1").sprite
move_right_animation = Animation(duration=10, frames=Player.move_right())


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
    is_space_pressed = keys[pygame.K_SPACE]

    on_ground = False
    prev_x = player_rect.x

    if is_right_pressed:
        player_rect.x += 2
        facing_dir = "right"
    elif is_left_pressed:
        player_rect.x -= 2
        facing_dir = "left"
    else:
        facing_dir = "front"

    collision_x(platforms, player_rect, prev_x)

    prev_top = player_rect.top
    prev_bottom = player_rect.bottom

    player_rect.y += player_velocity_y * dt  # y
    player_velocity_y += gravity * dt  # dy

    player_velocity_y, on_ground = collision_y(platforms, player_rect, player_velocity_y, prev_top, prev_bottom)

    if space_down_this_frame and jumps_left > 0:
        jumps_left -= 1
        player_velocity_y = -0.4
        on_ground = False
    elif on_ground:
        jumps_left = 2
    if not on_ground:
        if facing_dir == "right":
            player_img = player_right2
        elif facing_dir == "left":
            player_img = player_left2
        else:
            player_img = player.sprite
    else:
        if facing_dir == "right":
            move_right_animation.advance()
            player_img = move_right_animation.sprite
        elif facing_dir == "left":
            move_left_animation.advance()
            player_img = move_left_animation.sprite
        else:
            player_img = player.sprite

    background.draw(screen)
    for p in platforms:
        p.draw(screen)

    # screen.fill((0, 255, 0))
    screen.blit(player_img, player_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
