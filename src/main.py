import itertools
import sys
import traceback

import pygame

from gameplay.levels.dialog_box import DialogBox, DialogBoxView, make_dialog_rect
from gameplay.levels.level import Level
from gameplay.levels.levels_data import LEVEL_1_SPEC
from gameplay.levels.map.direction import Direction
from gameplay.levels.npcs import Npc
from gameplay.player.inventory import Inventory, InventoryUI
from gameplay.player.player import Player
from gameplay.player.player_mobility import PlayerMobility
from menu.ui import UIManager
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss
from screen.fps_counter import FPSCounter
from screen.game_inputs import GameInputs
from screen.layout import Layout
from screen.scale_screen import get_font_size


class Game:
    def __init__(self):
        self._init_pygame()
        self._init_game_window()
        self._init_display()
        self._init_dialogs()
        self._init_audio()
        self._init_game_inputs()
        self._init_inventory()
        self._init_gameplay()

    def _init_pygame(self):
        pygame.init()
        self.FPS = 60
        self.clock = pygame.time.Clock()

    def _init_game_window(self):
        game_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", target_height_px=64)
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption("Fruit World")

    def _init_display(self):
        self.ui = UIManager()
        self.fullscreen = False
        self.screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, self.fullscreen)
        self.game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
        self.font, self.font_size = get_font_size()
        self.layout = Layout(0.4 * self.font_size, 0.4 * self.font_size)
        self.fps_counter = FPSCounter(self.font)

    def _init_dialogs(self):
        rect = make_dialog_rect(int(ss.GAME_WIDTH), ss.SCREEN_HEIGHT, ss.DIALOG_HEIGHT, screen_bottom_border_margin=1)
        self.dialog_vm = DialogBox(rect=rect, cps=45, padding=self.font_size - 3)
        self.dialog_view = DialogBoxView(font=self.font)

    def _init_audio(self):
        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
        self.mhmm_sound = pygame.mixer.Sound("sounds/npc_mmhm.wav")

    def _init_game_inputs(self):
        self.inputs = GameInputs(self.game_surface, self.screen, self.layout, self.fullscreen, self.jump_sound)

    def _init_inventory(self):
        icon_height = ss.relative_y_to_game_units_px(0.05)
        strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", icon_height)
        blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", icon_height)
        item_icons = {
            "strawberry": strawberry_icon,
            "blueberry": blueberry_icon,
        }
        self.inventory = Inventory()
        self.inventory_ui = InventoryUI(self.font, item_icons, self.inputs.layout.right_window)

    def _init_gameplay(self):
        self.gravity = ss.game_units_to_decimal(0.001)
        self.sara = Player.load()
        self.move_player = PlayerMobility(self.gravity)
        self.level = Level(self.inventory, LEVEL_1_SPEC)
        self.away = True
        self.colliding_npc: Npc | None = None

    # noinspection PyAttributeOutsideInit
    def run(self):
        while self.inputs.running:
            try:
                dt = self.clock.tick_busy_loop(self.FPS)
                self.fps_counter.update(dt)
                now_ms = pygame.time.get_ticks()
                self.inputs.keyboard_roles()
                self.dialog_vm.handle_event(
                    self.inputs.is_pick_pressed, self.inputs.is_exit_pressed, self.away, now_ms, dt
                )

                for npc in self.level.current_map.npcs:
                    if self.sara.player_rect.colliderect(npc.npc_rect):
                        self.away = False
                        self.colliding_npc = npc
                        if self.inputs.is_pick_pressed:
                            self.mhmm_sound.play()
                            dialog_step = npc.interaction(now_ms)
                            self.dialog_vm.show(dialog_step, npc=npc)
                    else:
                        self.away = True
                    npc.update_sprite(now_ms, dt)

                if self.inputs.is_right_pressed:
                    self.move_player.move_right(self.level.current_map.platforms, dt)
                elif self.inputs.is_left_pressed:
                    self.move_player.move_left(self.level.current_map.platforms, dt)

                if self.inputs.space_down_this_frame:
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
                    self.inputs.is_right_pressed,
                    self.inputs.is_left_pressed,
                    self.move_player.coordinates,
                    dt,
                )

                self.inputs.screen.fill((53, 71, 46))  # tło gry
                self.level.draw_level(self.inputs.game_surface, self.sara)
                if self.inputs.DEBUG_OVERLAYS:
                    self.level.draw_debug(self.inputs.game_surface, self.move_player)

                # WYŚRODKOWANA gra:
                self.inputs.screen.blit(self.inputs.game_surface, self.inputs.layout.game_view.topleft)
                self.inputs.layout.draw_panel(self.inputs.screen)
                self.inputs.layout.draw_panel_windows(self.inputs.screen)
                # DIALOG:
                self.dialog_view.draw(self.inputs.screen, self.dialog_vm)
                # PRZEDMIOTY:
                if self.inputs.is_pick_pressed:
                    for bush in itertools.chain(
                        self.level.current_map.strawberry_bushes, self.level.current_map.blueberry_bushes
                    ):
                        picked_items = bush.try_pick_berries(self.sara.player_rect)
                        if picked_items > 0:
                            self.inventory.add(bush.berry_item_id, picked_items)

                self.inventory_ui.draw(self.inputs.screen, self.inventory)

                if self.inputs.DEBUG_OVERLAYS:
                    self.fps_counter.draw(self.inputs.screen)
                pygame.display.flip()

            except Exception as e:
                print(e)
                traceback.print_exc()
                input("czekamy")

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
