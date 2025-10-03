import pygame
import sys

from bushes import spawn_berries_for_bushes, draw_bush_debug
from player import Player
from maps_data import load_level
from berry import pick_berry
from player_mobility import PlayerMobility, draw_rect_debug
from dialog_box import DialogBox

DEBUG_OVERLAYS = False
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 720
FPS = 60
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
gravity = 0.001
font = pygame.font.SysFont("comicsansms", 18)
dialog = DialogBox(SCREEN_WIDTH, SCREEN_HEIGHT, font,
                   text_color=(0,0,0), bg_color=(255,255,255))
sara = Player.load()
move_player = PlayerMobility(gravity)
background, platforms, strawberry_bushes, blueberry_bushes, npcs, static_objects = load_level("map1")
strawberries_collected = 0
blueberries_collected = 0

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
    try:
        dt = clock.tick(FPS)  # ms od poprzedniej klatki
        now_ms = pygame.time.get_ticks()
        space_down_this_frame = False
        is_pick_pressed = False
        is_exit_pressed = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                space_down_this_frame = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                is_pick_pressed = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_0:
                DEBUG_OVERLAYS = not DEBUG_OVERLAYS
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                is_exit_pressed = True
            dialog.handle_event(is_pick_pressed, is_exit_pressed)

        keys = pygame.key.get_pressed()
        is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

        strawberries_collected += pick_berry(strawberries, sara.player_rect, is_pick_pressed)
        blueberries_collected += pick_berry(blueberries, sara.player_rect, is_pick_pressed)

        for npc in npcs:
            if sara.player_rect.colliderect(npc.npc_rect):
                if is_pick_pressed:
                    message = npc.interaction(now_ms)
                    dialog.show(message)
            else:
                message = npc.end_interaction(now_ms)
                dialog.show(message)
            npc.update_sprite(now_ms)

        prev_left = move_player.player_rect2.left
        prev_right = move_player.player_rect2.right

        if is_right_pressed:
            move_player.move_right(platforms)
        elif is_left_pressed:
            move_player.move_left(platforms)

        if space_down_this_frame:
            move_player.jump()

        dialog.update(dt)
        move_player.move_vertically(platforms, dt)
        sara.update_sprite(move_player.is_on_ground(), is_right_pressed, is_left_pressed, move_player.get_coordinates())



        screen.fill((67, 39, 15, 230))
        background.draw(screen)
        for platform in platforms:
            platform.draw(screen)

        for strawberry in strawberries:
            strawberry.draw(screen)
        for blueberry in blueberries:
            blueberry.draw(screen)
        for obj in static_objects:
            obj.draw(screen)
        for npc in npcs:
            npc.draw(screen)
        sara.draw(screen)
        dialog.draw(screen)

        if DEBUG_OVERLAYS:
            draw_bush_debug(screen, font, strawberry_bushes, (0, 200, 0), "TRUS")
            draw_bush_debug(screen, font, blueberry_bushes, (60, 120, 255), "BOR")
            small_font = pygame.font.SysFont("comicsansms", 10)  # było np. 18
            draw_rect_debug(screen, small_font, move_player.player_rect2, (0, 200, 0), "HIT")
            draw_rect_debug(screen, small_font, move_player.player_rect3, (0, 0, 200), "HIT")

        counter_text1 = font.render(f"Truskawki: {strawberries_collected}", True, (255, 255, 255))
        counter_text2 = font.render(f"Borówki: {blueberries_collected}", True, (255, 255, 255))

        screen.blit(counter_text1, (10, 550))
        screen.blit(counter_text2, (10, 570))

        pygame.display.flip()

    except Exception as e:
        print(e)
        input("czekamy")

pygame.quit()
sys.exit()
