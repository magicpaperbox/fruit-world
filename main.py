import pygame
import sys

from bushes import spawn_berries_for_bushes, draw_bush_debug
from player import Player
from maps_data import load_level
from collisions import collision_x, collision_y
from berry import pick_berry

DEBUG_OVERLAYS = False
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001
font = pygame.font.SysFont("comicsansms", 18)
sara = Player.load()
background, platforms, strawberry_bushes, blueberry_bushes, npcs, static_objects = load_level("map1")
strawberries_collected = 0
blueberries_collected = 0

player_velocity_y = 0
jumps_left = 2

strawberries = spawn_berries_for_bushes(
    strawberry_bushes,
    per_bush=3,
    sprite="strawberry",
    height_px=25
)
blueberries = spawn_berries_for_bushes(
    blueberry_bushes,
    per_bush=1,
    sprite="blueberry",
    height_px=20
)

running = True
while running:
    dt = clock.tick(FPS)  # ms od poprzedniej klatki

    space_down_this_frame = False
    is_pick_pressed = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            space_down_this_frame = True
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
            is_pick_pressed = True
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_0:
            DEBUG_OVERLAYS = not DEBUG_OVERLAYS

    keys = pygame.key.get_pressed()
    is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

    on_ground = False
    prev_x = sara.player_rect.x

    strawberries_collected += pick_berry(strawberries, sara.player_rect, is_pick_pressed)
    blueberries_collected += pick_berry(blueberries, sara.player_rect, is_pick_pressed)
    for npc in npcs:
        npc.update_sprite()

    if is_right_pressed:
        sara.player_rect.x += 2
    elif is_left_pressed:
        sara.player_rect.x -= 2

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

    sara.update_sprite(on_ground, is_right_pressed, is_left_pressed)

    background.draw(screen)
    for platform in platforms:
        platform.draw(screen)

    if DEBUG_OVERLAYS:
        draw_bush_debug(screen, font, strawberry_bushes, (0, 200, 0), "TRUS")
        draw_bush_debug(screen, font, blueberry_bushes, (60, 120, 255), "BOR")

    for strawberry in strawberries:
        strawberry.draw(screen)
    for blueberry in blueberries:
        blueberry.draw(screen)
    for obj in static_objects:
        obj.draw(screen)
    for npc in npcs:
        npc.draw(screen)
    sara.draw(screen)


    counter_text1 = font.render(f"Truskawki: {strawberries_collected}", True, (255, 255, 255))
    counter_text2 = font.render(f"Borówki: {blueberries_collected}", True, (255, 255, 255))

    screen.blit(counter_text1, (10, 550))
    screen.blit(counter_text2, (10, 570))

    pygame.display.flip()

pygame.quit()
sys.exit()
