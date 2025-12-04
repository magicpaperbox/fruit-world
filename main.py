import pygame
import sys

from bushes import spawn_berries_for_bushes, draw_bush_debug
from player import Player
from maps_data import load_level
from berry import pick_berry
from player_mobility import PlayerMobility, draw_rect_debug
from dialog_box import DialogBox
from ui import UIManager, Action
from settings_menu import toggle_settings, make_settings_modal
import scale_screen

DEBUG_OVERLAYS = False
SCREEN_WIDTH, SCREEN_HEIGHT = scale_screen.chosen_size
FPS = 60
pygame.init()
ui = UIManager()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GAME_WIDTH = scale_screen.GAME_WIDTH
GAME_HEIGHT = scale_screen.GAME_HEIGHT
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

clock = pygame.time.Clock()
gravity = 0.001
font = pygame.font.SysFont("comicsansms", 18)
dialog = DialogBox(GAME_WIDTH, SCREEN_HEIGHT, font,
                   text_color=(61,43,31), bg_color=(255,255,247), margin=0)
sara = Player.load()
move_player = PlayerMobility(gravity)
background, platforms, strawberry_bushes, blueberry_bushes, npcs, static_objects = load_level("map1")
strawberries_collected = 0
blueberries_collected = 0
away = True
colliding_npc = None

strawberries = spawn_berries_for_bushes(
    strawberry_bushes,
    per_bush=3,
    sprite="strawberry",
    height_px=scale_screen.GAME_HEIGHT*0.04
)
blueberries = spawn_berries_for_bushes(
    blueberry_bushes,
    per_bush=1,
    sprite="blueberry",
    height_px=scale_screen.GAME_HEIGHT*0.04
)


running = True
while running:
    try:
        dt = clock.tick(FPS)  # ms od poprzedniej klatki
        now_ms = pygame.time.get_ticks()
        space_down_this_frame = False
        is_pick_pressed = False
        is_exit_pressed = False
        settings_pressed = False

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
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                settings_pressed = True
            dialog.handle_event(is_pick_pressed, is_exit_pressed, away, now_ms)

        keys = pygame.key.get_pressed()
        is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

        strawberries_collected += pick_berry(strawberries, sara.player_rect, is_pick_pressed)
        blueberries_collected += pick_berry(blueberries, sara.player_rect, is_pick_pressed)


        for npc in npcs:
            if sara.player_rect.colliderect(npc.npc_rect):
                away = False
                colliding_npc = npc
                if is_pick_pressed:
                    message = npc.interaction(now_ms)
                    dialog.show(message, npc=npc)
            else:
                away = True
            npc.update_sprite(now_ms)


        prev_left = move_player.player_rect2.left
        prev_right = move_player.player_rect2.right

        if is_right_pressed:
            move_player.move_right(platforms, dt)
        elif is_left_pressed:
            move_player.move_left(platforms, dt)

        if space_down_this_frame:
            move_player.jump()

        dialog.update(dt)
        move_player.move_vertically(platforms, dt)
        sara.update_sprite(move_player.is_on_ground, is_right_pressed, is_left_pressed, move_player.coordinates)

        screen.fill((67, 39, 15))  # tło gry

        background.draw(game_surface)
        for platform in platforms:
            platform.draw(game_surface)

        for strawberry in strawberries:
            strawberry.draw(game_surface)
        for blueberry in blueberries:
            blueberry.draw(game_surface)
        for obj in static_objects:
            obj.draw(game_surface)
        for npc in npcs:
            npc.draw(game_surface)
        sara.draw(game_surface)

        if DEBUG_OVERLAYS:
            draw_bush_debug(game_surface, font, strawberry_bushes, (0, 200, 0), "TRUS")
            draw_bush_debug(game_surface, font, blueberry_bushes, (60, 120, 255), "BOR")
            small_font = pygame.font.SysFont("comicsansms", 10)
            draw_rect_debug(game_surface, small_font, move_player.player_rect2, (0, 200, 0), "HIT")
            draw_rect_debug(game_surface, small_font, move_player.player_rect3, (0, 0, 200), "HIT")

        counter_text1 = font.render(f"Truskawki: {strawberries_collected}", True, (255, 255, 255))
        counter_text2 = font.render(f"Borówki: {blueberries_collected}", True, (255, 255, 255))
        game_surface.blit(counter_text1, (10, 550))
        game_surface.blit(counter_text2, (10, 570))

        screen_w, screen_h = screen.get_size()
        offset_x = (screen_w - GAME_WIDTH) // 2
        offset_y = 0

        # WYŚRODKOWANA gra:
        screen.blit(game_surface, (offset_x, offset_y))

        # RYSUJEMY DIALOG NA DOLE:
        dialog.rect.y = GAME_HEIGHT
        dialog.rect.x = (SCREEN_WIDTH - GAME_WIDTH)//2
        dialog.draw(screen)

        pygame.display.flip()

    except Exception as e:
        print(e)
        input("czekamy")

pygame.quit()
sys.exit()
