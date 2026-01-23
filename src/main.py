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


# noinspection PyAttributeOutsideInit
class Game:
    def __init__(self):
        self._init_pygame()
        self._init_display()
        self._init_dialogs()
        self._init_audio()
        self._init_game_control()
        self._init_icons()
        self._init_inventory()
        self._init_gameplay()

    def _init_pygame(self):
        self.FPS = 60
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

    def _init_display(self):
        self.gravity = ss.game_units_to_decimal(0.001)
        self.ui = UIManager()
        self.fullscreen = False
        self.screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, self.fullscreen)
        self.game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
        self.font, self.font_size = get_font_size()
        self.layout = Layout(0.4 * self.font_size, 0.4 * self.font_size)

    def _init_dialogs(self):
        self.rect = make_dialog_rect(
            int(ss.GAME_WIDTH), ss.SCREEN_HEIGHT, ss.DIALOG_HEIGHT, screen_bottom_border_margin=1
        )
        self.dialog_vm = DialogBox(rect=self.rect, cps=45, padding=self.font_size - 3)
        self.dialog_view = DialogBoxView(font=self.font)

    def _init_audio(self):
        self.jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
        self.mhmm = pygame.mixer.Sound("sounds/npc_mmhm.wav")

    def _init_game_control(self):
        self.control = Control(self.game_surface, self.screen, self.layout, self.fullscreen, self.jump_sound)
        self.fps_counter = FPSCounter(self.font)

    def _init_icons(self):
        self.ICON_HEIGHT = ss.relative_y_to_game_units_px(0.05)
        self.strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", self.ICON_HEIGHT)
        self.blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", self.ICON_HEIGHT)
        self.item_icons = {
            "strawberry": self.strawberry_icon,
            "blueberry": self.blueberry_icon,
        }
        pygame.display.set_icon(self.strawberry_icon)
        pygame.display.set_caption("Fruit world")

    def _init_inventory(self):
        self.inventory = Inventory()
        self.inventory_ui = InventoryUI(self.font, self.item_icons, self.control.layout.right_window)

    def _init_gameplay(self):
        self.sara = Player.load()
        self.move_player = PlayerMobility(self.gravity)
        self.level = Level(self.inventory, LEVEL_1_SPEC)
        self.away = True
        self.colliding_npc = None

    def run(self):
        while self.control.running:
            try:
                dt = self.clock.tick_busy_loop(self.FPS)
                self.fps_counter.update(dt)
                now_ms = pygame.time.get_ticks()
                self.control.keyboard_roles()
                self.dialog_vm.handle_event(
                    self.control.is_pick_pressed, self.control.is_exit_pressed, self.away, now_ms, dt
                )

                for npc in self.level.current_map.npcs:
                    if self.sara.player_rect.colliderect(npc.npc_rect):
                        self.away = False
                        self.colliding_npc = npc
                        if self.control.is_pick_pressed:
                            self.mhmm.play()
                            dialog_step = npc.interaction(now_ms)
                            self.dialog_vm.show(dialog_step, npc=npc)
                    else:
                        self.away = True
                    npc.update_sprite(now_ms, dt)

                if self.control.is_right_pressed:
                    self.move_player.move_right(self.level.current_map.platforms, dt)
                elif self.control.is_left_pressed:
                    self.move_player.move_left(self.level.current_map.platforms, dt)

                if self.control.space_down_this_frame:
                    self.move_player.jump()

                self.dialog_vm.update(dt)
                self.move_player.move_vertically(self.level.current_map.platforms, dt)

                if self.move_player.visual_rect.centerx > ss.GAME_WIDTH:
                    if self.level.try_load_map(Direction.RIGHT):
                        self.move_player.set_x_position(0)
                    else:
                        reset_player = ss.GAME_WIDTH - self.sara.player_rect.width
                        self.move_player.set_x_position(reset_player)
                elif self.move_player.visual_rect.centerx <= 0:
                    if self.level.try_load_map(Direction.LEFT):
                        reset_player = ss.GAME_WIDTH - self.sara.player_rect.width
                        self.move_player.set_x_position(reset_player)
                    else:
                        self.move_player.set_x_position(0)

                self.sara.update_sprite(
                    self.move_player.is_on_ground,
                    self.control.is_right_pressed,
                    self.control.is_left_pressed,
                    self.move_player.coordinates,
                    dt,
                )

                self.control.screen.fill((53, 71, 46))  # tło gry
                self.level.draw_level(self.control.game_surface, self.sara)
                if self.control.DEBUG_OVERLAYS:
                    self.level.draw_debug(self.control.game_surface, self.move_player)

                # screen_w, screen_h = self.control.screen.get_size()
                # offset_x = (screen_w - ss.GAME_WIDTH) // 2
                # offset_y = 0

                # WYŚRODKOWANA gra:
                self.control.screen.blit(self.control.game_surface, self.control.layout.game_view.topleft)
                self.control.layout.draw_panel(self.control.screen)
                self.control.layout.draw_panel_windows(self.control.screen)
                # DIALOG:
                self.dialog_view.draw(self.control.screen, self.dialog_vm)
                # PRZEDMIOTY:
                if self.control.is_pick_pressed:
                    for bush in itertools.chain(
                        self.level.current_map.strawberry_bushes, self.level.current_map.blueberry_bushes
                    ):
                        picked_items = bush.try_pick_berries(self.sara.player_rect)
                        if picked_items > 0:
                            self.inventory.add(bush.berry_item_id, picked_items)

                self.inventory_ui.draw(self.control.screen, self.inventory)

                if self.control.DEBUG_OVERLAYS:
                    self.fps_counter.draw(self.control.screen)
                pygame.display.flip()

            except Exception as e:
                print(e)
                traceback.print_exc()
                # traceback.print_tb(e)
                input("czekamy")

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
