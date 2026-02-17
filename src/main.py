import ctypes
import itertools
import sys
import traceback

import pygame

from gameplay.game_over_screen import GameOverScreen
from gameplay.levels.consumables.consumable import Consumable
from gameplay.levels.dialog_box import DialogBox, DialogBoxView, make_dialog_rect
from gameplay.levels.hazards import Hazard
from gameplay.levels.level import Level
from gameplay.levels.levels_data import LEVEL_1_SPEC
from gameplay.levels.music import Music
from gameplay.levels.npcs import Npc
from gameplay.player.inventory import InventoryUI
from gameplay.player.player import Player
from gameplay.resources_ui import ResourcesUI
from menu.main_menu import MainMenu
from menu.settings_menu import GameSettings
from menu.ui.ui_manager import UIManager
from render.effect_manager import EffectManager
from render.lighting import Lighting, SunLight
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss
from screen.fonts import FontsFactory, FontSize, FontStyle
from screen.fps_counter import FPSCounter
from screen.game_inputs import GameInputs
from screen.game_units import RelativeUnit
from screen.layout import Layout


class Game:
    def __init__(self):
        self._init_pygame()
        self._init_display()
        self._init_game_window()
        self._init_dialogs()
        self._init_audio()
        self._init_game_inputs()
        self._init_inventory()
        self._init_gameplay()

    def _init_pygame(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
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
        self.fonts = FontsFactory()
        self.layout = Layout()
        self.resources_ui = ResourcesUI(self.fonts.get_font(FontSize.LARGE, FontStyle.HANDWRITTING))
        self.fps_counter = FPSCounter(self.fonts.get_font(FontSize.LARGE, FontStyle.SIMPLE))
        self.lighting = Lighting(ss.GAME_WIDTH, ss.GAME_HEIGHT)
        self.sunlight = SunLight()

    def _init_dialogs(self):
        rect = make_dialog_rect(ss.GAME_WIDTH, ss.GAME_HEIGHT)
        self.dialog_vm = DialogBox(rect=rect)
        self.dialog_view = DialogBoxView(font=self.fonts.get_font(FontSize.LARGE, FontStyle.SIMPLE))

    def _init_audio(self):
        pygame.mixer.init()
        self.music = Music()
        self.jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
        self.mhmm_sound = pygame.mixer.Sound("sounds/npc_mmhm.wav")

    def _change_volume(self, val):
        pygame.mixer.music.set_volume(val)

    def _init_game_inputs(self):
        self.game_over_screen = GameOverScreen(self.fonts.get_font(FontSize.XLARGE, FontStyle.CAPS_CONDENSED_BOLD))
        main_menu = MainMenu(self.screen.get_size(), self.fonts.get_font(FontSize.LARGE, FontStyle.CAPS_CONDENSED))  # ?
        self.settings = GameSettings(
            self.fonts.get_font(FontSize.XLARGE, FontStyle.CAPS_CONDENSED_BOLD), change_volume_callback=self._change_volume
        )
        self.inputs = GameInputs(
            self.game_surface, self.screen, self.layout, self.fullscreen, self.jump_sound, main_menu, self.game_over_screen, self.settings
        )

    def _init_inventory(self):
        icon_height = RelativeUnit(0.03).pixels_y
        strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", icon_height)
        blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", icon_height)
        item_icons = {
            "strawberry": strawberry_icon,
            "blueberry": blueberry_icon,
        }
        self.inventory_ui = InventoryUI(
            self.fonts.get_font(FontSize.MEDIUM, FontStyle.HANDWRITTING), item_icons, self.inputs.layout.right_window
        )

    def _init_gameplay(self):
        self.gravity = ss.game_units_to_decimal(0.001)
        self.sara = Player.load(self.gravity)
        self.hazard = Hazard()
        self.level = Level(self.sara.inventory, LEVEL_1_SPEC)
        self.away = True
        self.colliding_npc: Npc | None = None
        self.effect_manager = EffectManager()

    def _update_gameplay(self, dt: int):
        self.music.play(self.level.music_path)
        self.dialog_vm.handle_event(self.inputs.is_interaction_pressed, self.inputs.is_exit_pressed, self.away, dt)

        for npc in self.level.current_map.npcs:
            if self.sara.player_rect.colliderect(npc.npc_rect):
                self.away = False
                self.colliding_npc = npc
                if self.inputs.is_interaction_pressed:
                    self.mhmm_sound.play()
                    dialog_step = npc.interaction()
                    if dialog_step is not None:
                        self.dialog_vm.show(dialog_step, npc=npc)
            else:
                self.away = True
                self.colliding_npc = None
            npc.update_sprite(dt)
        self.dialog_vm.update(dt)

        self.hazard.update(dt)
        self.hazard.collide_hazard(self.level.current_map.hazard, self.sara.player_rect, self.sara.health)
        if self.sara.health.is_dead:
            self.inputs.is_game_over = True
        all_solids = self.level.current_map.platforms + self.level.current_map.hazard
        is_npc_talking = self.colliding_npc is not None and self.colliding_npc.is_talking
        if is_npc_talking:
            self.inputs.block_movement()
        else:
            self.inputs.unblock_movement()
        self.sara.process_inputs(dt, self.inputs, all_solids)
        self.sara.update_sprite(self.inputs, dt)
        self.level.change_map(self.sara)
        Consumable.consume(self.level.current_map.consumable_objects, self.sara, self.effect_manager)
        if self.inputs.is_interaction_pressed:
            for bush in itertools.chain(self.level.current_map.strawberry_bushes, self.level.current_map.blueberry_bushes):
                picked_items = bush.try_pick_berries(self.sara.player_rect)
                if picked_items > 0:
                    self.sara.inventory.add(bush.berry_item_id, picked_items)
        self.sunlight.update(dt)
        self.level.update_level(dt)
        self.effect_manager.update(dt)

    def _draw_gameplay(self):
        self.inputs.screen.fill((53, 71, 46))
        game_screen = self.inputs.game_surface
        self.level.draw_level(game_screen)
        if self.colliding_npc is not None and self.colliding_npc.has_something_to_say():
            self.colliding_npc.draw_bubble(game_screen, player_nearby=True)
        self.sara.draw(game_screen)
        self.effect_manager.draw(game_screen)
        self.sunlight.draw(game_screen)
        self.lighting.reset()
        # self.lighting.draw_light(self.sara.player_rect.center)
        self.lighting.apply(game_screen)
        if self.inputs.DEBUG_OVERLAYS:
            self.level.draw_debug(game_screen, [self.sara])

        self.inputs.screen.blit(game_screen, self.inputs.layout.game_view.topleft)
        self.inputs.layout.draw_panel(self.inputs.screen)
        self.inputs.layout.draw_panel_windows(self.inputs.screen)
        self.dialog_view.draw(self.inputs.screen, self.dialog_vm)
        self.inventory_ui.draw(self.inputs.screen, self.sara.inventory)
        self.resources_ui.draw(self.inputs.screen, self.sara.money, self.sara.health, self.sara.mana)

        if self.inputs.DEBUG_OVERLAYS:
            self.fps_counter.draw(self.inputs.screen)

    def run(self):
        while self.inputs.game_loop_running:
            try:
                dt = self.clock.tick_busy_loop(self.FPS)
                self.fps_counter.update(dt)
                self.inputs.process_inputs()

                if self.inputs.reset_level:
                    self._init_gameplay()
                    self.inputs.reset_level = False
                if self.inputs.in_menu:
                    self.music.play("sounds/music/Fruit World.mp3")
                    self.inputs.main_menu.draw(self.inputs.screen)
                elif self.inputs.is_game_over:
                    self.game_over_screen.draw(self.screen)
                elif self.inputs.in_settings:
                    self._draw_gameplay()
                    self.settings.draw(self.screen)
                else:
                    self._update_gameplay(dt)
                    self._draw_gameplay()

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
