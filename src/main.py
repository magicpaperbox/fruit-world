import itertools
import sys
import traceback

import pygame

from gameplay.levels.level import Level
from gameplay.levels.levels_data import LEVEL_1_SPEC
from gameplay.levels.map.direction import Direction
from screen import scale_screen as ss
from gameplay.levels.dialog_box import DialogBox, DialogBoxView, make_dialog_rect
from gameplay.player.inventory import Inventory, InventoryUI
from screen.layout import Layout
from gameplay.player.player import Player
from gameplay.player.player_mobility import PlayerMobility
from render.sprite_factory import SPRITE_FACTORY
from screen.scale_screen import get_font_size
from menu.ui import UIManager
from screen.control import Control
from screen.fps_counter import FPSCounter

FPS = 0
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
gravity = ss.game_units_to_decimal(0.001)
ui = UIManager()

fullscreen = False
screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, fullscreen)
game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
font, font_size = get_font_size()
layout = Layout(0.4 * font_size, 0.4 * font_size)
rect = make_dialog_rect(int(ss.GAME_WIDTH), ss.SCREEN_HEIGHT, ss.DIALOG_HEIGHT, screen_bottom_border_margin=1)
dialog_vm = DialogBox(rect=rect, cps=45, padding=font_size - 3)
dialog_view = DialogBoxView(font=font)
jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
mhmm = pygame.mixer.Sound("sounds/npc_mmhm.wav")

control = Control(game_surface, screen, layout, fullscreen, dialog_vm, jump_sound)
fps_counter = FPSCounter(font)

ICON_HEIGHT = ss.relative_y_to_game_units_px(0.05)
strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", ICON_HEIGHT)
blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", ICON_HEIGHT)
item_icons = {
    "strawberry": strawberry_icon,
    "blueberry": blueberry_icon,
}

pygame.display.set_icon(strawberry_icon)
pygame.display.set_caption("Fruit world")

inventory = Inventory()
inventory_ui = InventoryUI(font, item_icons, control.layout.right_window)
sara = Player.load()
move_player = PlayerMobility(gravity)
level = Level(inventory, LEVEL_1_SPEC)
away = True
colliding_npc = None

while control.running:
    try:
        dt = clock.tick_busy_loop(FPS)
        fps_counter.update(dt)
        now_ms = pygame.time.get_ticks()
        control.keyboard_roles(dt, now_ms, away)

        for npc in level.current_map.npcs:
            if sara.player_rect.colliderect(npc.npc_rect):
                away = False
                colliding_npc = npc
                if control.is_pick_pressed:
                    mhmm.play()
                    dialog_step = npc.interaction(now_ms)
                    dialog_vm.show(dialog_step, npc=npc)
            else:
                away = True
            npc.update_sprite(now_ms, dt)

        if control.is_right_pressed:
            move_player.move_right(level.current_map.platforms, dt)
        elif control.is_left_pressed:
            move_player.move_left(level.current_map.platforms, dt)

        if control.space_down_this_frame:
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
            control.is_right_pressed,
            control.is_left_pressed,
            move_player.coordinates,
            dt
        )

        control.screen.fill((53, 71, 46))  # tło gry
        level.draw_level(control.game_surface, sara)
        if control.DEBUG_OVERLAYS:
            level.draw_debug(control.game_surface, move_player)

        screen_w, screen_h = control.screen.get_size()
        offset_x = (screen_w - ss.GAME_WIDTH) // 2
        offset_y = 0

        # WYŚRODKOWANA gra:
        control.screen.blit(control.game_surface, control.layout.game_view.topleft)
        control.layout.draw_panel(control.screen)
        control.layout.draw_panel_windows(control.screen)
        # DIALOG:
        dialog_view.draw(control.screen, dialog_vm)
        # PRZEDMIOTY:
        if control.is_pick_pressed:
            for bush in itertools.chain(level.current_map.strawberry_bushes, level.current_map.blueberry_bushes):
                picked_items = bush.try_pick_berries(sara.player_rect)
                if picked_items > 0:
                    inventory.add(bush.berry_item_id, picked_items)

        inventory_ui.draw(control.screen, inventory)

        if control.DEBUG_OVERLAYS:
            fps_counter.draw(control.screen)
        pygame.display.flip()

    except Exception as e:
        print(e)
        traceback.print_tb(e)
        input("czekamy")

pygame.quit()
sys.exit()
