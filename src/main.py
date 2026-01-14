import itertools
import sys
import traceback

import pygame

from gameplay.levels.level import Level
from gameplay.levels.levels_data import LEVEL_1_SPEC
from gameplay.levels.map.direction import Direction
from screen import scale_screen as ss
from render.debug import draw_rect, draw_area
from gameplay.levels.dialog_box import DialogBox, DialogBoxView, make_dialog_rect
from gameplay.player.inventory import Inventory, InventoryUI
from screen.layout import Layout
from gameplay.player.player import Player
from gameplay.player.player_mobility import PlayerMobility
from render.sprite_factory import SPRITE_FACTORY
from screen.scale_screen import get_font_size
from menu.ui import UIManager

DEBUG_OVERLAYS = False
FPS = 60
pygame.init()
ui = UIManager()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
fall = pygame.mixer.Sound("sounds/jump_rustle.wav").play()
fullscreen = False

screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, fullscreen)
game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
ICON_HEIGHT = ss.relative_y_to_game_units_px(0.05)
strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", ICON_HEIGHT)
blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", ICON_HEIGHT)
item_icons = {
    "strawberry": strawberry_icon,
    "blueberry": blueberry_icon,
}

pygame.display.set_icon(strawberry_icon)
pygame.display.set_caption("Fruit world")

clock = pygame.time.Clock()
gravity = ss.game_units_to_decimal(0.001)

font, font_size = get_font_size()
layout = Layout(0.4 * font_size, 0.4 * font_size)
rect = make_dialog_rect(int(ss.GAME_WIDTH), ss.SCREEN_HEIGHT, ss.DIALOG_HEIGHT, screen_bottom_border_margin=1)
dialog_vm = DialogBox(rect=rect, cps=45, padding=font_size - 3)
dialog_view = DialogBoxView(font=font)

inventory = Inventory()
inventory_ui = InventoryUI(font, item_icons, layout.right_window)
sara = Player.load()
move_player = PlayerMobility(gravity)
level = Level(inventory, LEVEL_1_SPEC)
away = True
colliding_npc = None

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
                layout = Layout(16, 16)
                game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
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
        dialog_vm.handle_event(is_pick_pressed, is_exit_pressed, away, now_ms, dt)
        keys = pygame.key.get_pressed()
        is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

        for npc in level.current_map.npcs:
            if sara.player_rect.colliderect(npc.npc_rect):
                away = False
                colliding_npc = npc
                if is_pick_pressed:
                    pygame.mixer.Sound("sounds/npc_mmhm.wav").play()
                    dialog_step = npc.interaction(now_ms)
                    dialog_vm.show(dialog_step, npc=npc)
            else:
                away = True
            npc.update_sprite(now_ms)

        if is_right_pressed:
            move_player.move_right(level.current_map.platforms, dt)
        elif is_left_pressed:
            move_player.move_left(level.current_map.platforms, dt)

        if space_down_this_frame:
            move_player.jump()

        dialog_vm.update(dt)
        move_player.move_vertically(level.current_map.platforms, dt)

        if move_player.visual_rect.centerx > ss.GAME_WIDTH:
            if level.try_load_map(Direction.RIGHT):
                move_player.set_x_position(0)
            else:
                reset_player = ss.GAME_WIDTH - sara.player_rect.width
                move_player.set_x_position(reset_player)
        elif move_player.visual_rect.centerx <= 0:
            if level.try_load_map(Direction.LEFT):
                reset_player = ss.GAME_WIDTH - sara.player_rect.width
                move_player.set_x_position(reset_player)
            else:
                move_player.set_x_position(0)

        sara.update_sprite(
            move_player.is_on_ground,
            is_right_pressed,
            is_left_pressed,
            move_player.coordinates,
        )

        screen.fill((53, 71, 46))  # tło gry

        level.current_map.background_img.draw(game_surface)
        for platform in level.current_map.platforms:
            platform.draw(game_surface)
        for bush in level.current_map.blueberry_bushes:
            bush.draw(game_surface)
        for bush in level.current_map.strawberry_bushes:
            bush.draw(game_surface)
        for obj in level.current_map.static_objects:
            obj.draw(game_surface)
        for npc in level.current_map.npcs:
            npc.draw(game_surface)
        sara.draw(game_surface)

        if DEBUG_OVERLAYS:
            draw_area(game_surface, level.current_map.strawberry_bushes, (190, 20, 40), "TRUS")
            draw_area(game_surface, level.current_map.blueberry_bushes, (60, 120, 255), "BOR")
            draw_rect(game_surface, move_player.collision_rect_x, (250, 250, 0), "HIT")
            draw_rect(game_surface, move_player.collision_rect_y, (250, 165, 20), "HIT")
            for platform in level.current_map.platforms:
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
        # DIALOG:
        dialog_view.draw(screen, dialog_vm)
        # PRZEDMIOTY:
        if is_pick_pressed:
            for bush in itertools.chain(level.current_map.strawberry_bushes, level.current_map.blueberry_bushes):
                picked_items = bush.try_pick_berries(sara.player_rect)
                if picked_items > 0:
                    inventory.add(bush.berry_item_id, picked_items)

        inventory_ui.draw(screen, inventory)
        pygame.display.flip()

    except Exception as e:
        print(e)
        traceback.print_tb(e)
        input("czekamy")

pygame.quit()
sys.exit()
