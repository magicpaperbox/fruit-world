import pygame
import sys
from animation import Animation
from maps import Map
from platforms import Platform

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001

# class Player:
#     def __init__(self, dx: float, dy: float, image: str):
#         self.dx = dx
#         self.dy = dy
#         self.on_ground = on_ground
#         self.current_img = image


map_1 = Map.load("background_1")

my_platform1 = Platform(193, 60, 165, 260)
my_platform2 = Platform(212, 60, 477, 368)
my_platform3 = Platform(119, 55, 346, 78)
my_platform4 = Platform(380, 62, 0, 488)
my_platform5 = Platform(150, 62, 660, 488)
my_platform6 = Platform(800, 60, 0, 550)


def scale_player(player_sprite: pygame.surface.Surface) -> pygame.surface.Surface:
    original_height = player_sprite.get_height()
    original_width = player_sprite.get_width()
    target_height = 80
    player_scale = target_height / original_height
    target_width = player_scale * original_width
    return pygame.transform.smoothscale(player_sprite, (target_width, target_height))


def load_player_sprite(sprite_name: str) -> pygame.surface.Surface:
    sprite = pygame.image.load(f"sprites/player/{sprite_name}.png")
    return scale_player(sprite)


player_static = load_player_sprite("static")

player_img = player_static
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
player_velocity_y = 0
jumps_left = 2

player_left2 = load_player_sprite("left_1")
move_left_animation = Animation(duration=5, frames=[
    # load_player_sprite("left_1"),
    load_player_sprite("left_2"),
    load_player_sprite("left_3"),
    load_player_sprite("left_4"),
    # load_player_sprite("left_5")
])

player_right2 = load_player_sprite("right_1")
move_right_animation = Animation(duration=5, frames=[
    load_player_sprite("right_2"),
    load_player_sprite("right_3"),
    load_player_sprite("right_4"),
])
running = True
while running:
    dt = clock.tick(FPS)  # sekundy od poprzedniej klatki

    space_down_this_frame = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            space_down_this_frame = True

    keys = pygame.key.get_pressed()
    is_right_pressed = keys[pygame.K_d]
    is_left_pressed = keys[pygame.K_a]
    is_space_pressed = keys[pygame.K_SPACE]

    ground = 475

    # player_pos_y = player_rect.y
    # player_pos_x = player_rect.x
    on_ground = False

    if player_rect.y == ground:
        on_ground = True

    if space_down_this_frame and jumps_left > 0:
        jumps_left -= 1
        player_velocity_y = -0.4
        on_ground = False

    player_rect.y += player_velocity_y * dt  # y
    player_velocity_y += gravity * dt  # dy

    if player_rect.y >= ground:
        player_rect.y = ground
        player_velocity_y = 0
        on_ground = True
        jumps_left = 2

    if is_right_pressed:
        player_rect.x += 2
        if player_velocity_y != 0:
            player_img = player_right2
        else:
            move_right_animation.advance()
            player_img = move_right_animation.sprite

    elif is_left_pressed:
        player_rect.x -= 2
        if player_velocity_y != 0:
            player_img = player_left2
        else:
            move_left_animation.advance()
            player_img = move_left_animation.sprite

    else:
        player_img = player_static

    map_1.draw(screen)
    my_platform1.draw(screen)
    my_platform2.draw(screen)
    my_platform3.draw(screen)
    my_platform4.draw(screen)
    my_platform5.draw(screen)
    my_platform6.draw(screen)

    # screen.fill((0, 255, 0))
    screen.blit(player_img, player_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
