import sys

import pygame
from layout import Layout
from bushes import spawn_berries_for_bushes
from debug import draw_rect, draw_area
from dialog_box import DialogBox
from inventory import Inventory, InventoryUI
from item import pick_item, Item
from maps_data import load_level
from player import Player
from player_mobility import PlayerMobility
import scale_screen as ss
from ui import UIManager

DEBUG_OVERLAYS = False
FPS = 60
pygame.init()
ui = UIManager()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
fall = pygame.mixer.Sound("sounds/jump_rustle.wav").play()
fullscreen = False

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, fullscreen)
layout = Layout()
game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
# game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
raw_strawberry = pygame.image.load("sprites/items/strawberry.png").convert_alpha()
raw_blueberry = pygame.image.load("sprites/items/blueberry.png").convert_alpha()
ICON_HEIGHT = ss.relative_y_to_game_units_px(0.05)
strawberry_icon = Item.scale(raw_strawberry, ICON_HEIGHT)
blueberry_icon = Item.scale(raw_blueberry, ICON_HEIGHT)

item_icons = {
    "strawberry": strawberry_icon,
    "blueberry": blueberry_icon,
}

pygame.display.set_icon(strawberry_icon)
pygame.display.set_caption("Fruit world")

clock = pygame.time.Clock()
gravity = ss.game_units_to_decimal(0.001)
font = pygame.font.SysFont("comicsansms", 18)
dialog = DialogBox(
    ss.GAME_WIDTH,
    ss.SCREEN_HEIGHT,
    font,
    margin=0
)
sara = Player.load()
move_player = PlayerMobility(gravity)
background, platforms, strawberry_bushes, blueberry_bushes, npcs, static_objects = load_level("map1")
strawberries_collected = 0
blueberries_collected = 0
inventory = Inventory()
inventory_ui = InventoryUI(font, item_icons)
away = True
colliding_npc = None

strawberries = spawn_berries_for_bushes(
    strawberry_bushes,
    per_bush=3,
    sprite="strawberry",
)
blueberries = spawn_berries_for_bushes(
    blueberry_bushes,
    per_bush=1,
    sprite="blueberry",
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

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                fullscreen = not fullscreen
                screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, fullscreen)
                layout = Layout()
                game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()

                # dialog też ma rect zależny od szerokości
                dialog.rect.width = ss.GAME_WIDTH
                dialog.rect.x = 0
                dialog.rect.y = ss.GAME_HEIGHT

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                space_down_this_frame = True
                jump_sound.play().set_volume(0.9)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                is_pick_pressed = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_0:
                DEBUG_OVERLAYS = not DEBUG_OVERLAYS
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                is_exit_pressed = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                settings_pressed = True
        dialog.handle_event(is_pick_pressed, is_exit_pressed, away, now_ms, dt)

        keys = pygame.key.get_pressed()
        is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

        for npc in npcs:
            if sara.player_rect.colliderect(npc.npc_rect):
                away = False
                colliding_npc = npc
                if is_pick_pressed:
                    pygame.mixer.Sound("sounds/npc_mmhm.wav").play()
                    message = npc.interaction(now_ms)
                    dialog.show(message, npc=npc)
            else:
                away = True
            npc.update_sprite(now_ms)

        prev_left = move_player.collision_rect_x.left
        prev_right = move_player.collision_rect_x.right

        if is_right_pressed:
            move_player.move_right(platforms, dt)
        elif is_left_pressed:
            move_player.move_left(platforms, dt)

        if space_down_this_frame:
            move_player.jump()

        dialog.update(dt)
        move_player.move_vertically(platforms, dt)
        sara.update_sprite(
            move_player.is_on_ground,
            is_right_pressed,
            is_left_pressed,
            move_player.coordinates,
        )

        screen.fill((53, 71, 46))  # tło gry

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
            draw_area(game_surface, strawberry_bushes, (190, 20, 40), "TRUS")
            draw_area(game_surface, blueberry_bushes, (60, 120, 255), "BOR")
            draw_rect(game_surface, move_player.collision_rect_x, (250, 250, 0), "HIT")
            draw_rect(game_surface, move_player.collision_rect_y, (250, 165, 20), "HIT")
            for platform in platforms:
                draw_rect(
                    game_surface,
                    platform.rect,
                    (0, 230, 0),
                    f"{platform.rect.left}x{platform.rect.top}",
                )

        screen_w, screen_h = screen.get_size()
        offset_x = (screen_w - ss.GAME_WIDTH) // 2
        offset_y = 0

        # WYŚRODKOWANA gra:
        # screen.blit(game_surface, (offset_x, offset_y))
        screen.blit(game_surface, layout.game_view.topleft)
        layout.draw_panel(screen)
        layout.draw_panel_windows(screen)

        # DIALOGI:
        dialog.rect.y = ss.GAME_HEIGHT
        dialog.rect.x = (ss.SCREEN_WIDTH - ss.GAME_WIDTH) // 2
        dialog.draw(screen)

        # PRZEDMIOTY:
        picked_strawberries = pick_item(strawberries, sara.player_rect, is_pick_pressed)
        picked_blueberries = pick_item(blueberries, sara.player_rect, is_pick_pressed)

        if picked_strawberries:
            inventory.add("strawberry", picked_strawberries)

        if picked_blueberries:
            inventory.add("blueberry", picked_blueberries)

        inventory_ui.draw(screen, inventory, x=10, y=20)

        pygame.display.flip()

    except Exception as e:
        print(e)
        input("czekamy")

pygame.quit()
sys.exit()
