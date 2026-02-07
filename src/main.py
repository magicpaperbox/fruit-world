import itertools
import sys
import traceback

import pygame

from gameplay.game_over_screen import GameOverScreen
from gameplay.levels.dialog_box import DialogBox, DialogBoxView, make_dialog_rect
from gameplay.levels.level import Level
from gameplay.levels.levels_data import LEVEL_1_SPEC
from gameplay.levels.map.consumables import collect_consumables
from gameplay.levels.map.hazards import Hazard
from gameplay.levels.map.music import Music
from gameplay.levels.npcs import Npc
from gameplay.player.inventory import InventoryUI
from gameplay.player.player import Player
from gameplay.resources_ui import ResourcesUI
from menu.main_menu import MainMenu
from menu.ui import UIManager
from render.interaction_effects import Particle
from render.lighting import Lighting, SunLight
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss
from screen.fonts import FontsFactory, FontSize, FontStyle
from screen.fps_counter import FPSCounter
from screen.game_inputs import GameInputs
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
        self.font = FontsFactory()
        self.font_size = ss.game_units_to_px(6)
        self.layout = Layout()
        self.resources_ui = ResourcesUI(self.font.get_font(FontSize.XLARGE, FontStyle.RUSTIC))
        self.fps_counter = FPSCounter(self.font.get_font(FontSize.LARGE, FontStyle.SIMPLE))
        self.lighting = Lighting(ss.GAME_WIDTH, ss.GAME_HEIGHT)
        self.sunlight = SunLight()

    def _init_dialogs(self):
        rect = make_dialog_rect(ss.GAME_WIDTH, ss.GAME_HEIGHT)
        self.dialog_vm = DialogBox(rect=rect)
        self.dialog_view = DialogBoxView(font=self.font.get_font(FontSize.SMALL, FontStyle.SIMPLE))

    def _init_audio(self):
        pygame.mixer.init()
        self.music = Music()
        self.jump_sound = pygame.mixer.Sound("sounds/jump_rustle.wav")
        self.mhmm_sound = pygame.mixer.Sound("sounds/npc_mmhm.wav")

    def _init_game_inputs(self):
        self.game_over_screen = GameOverScreen(self.screen, self.font.get_font(FontSize.LARGE, FontStyle.ORNATE))
        main_menu = MainMenu(self.screen.get_size(), self.font.get_font(FontSize.LARGE, FontStyle.CAPS_CONDENSED))  # ?
        self.inputs = GameInputs(
            self.game_surface, self.screen, self.layout, self.fullscreen, self.jump_sound, main_menu, self.game_over_screen
        )

    def _init_inventory(self):
        icon_height = ss.relative_y_to_game_units_px(0.03)
        strawberry_icon = SPRITE_FACTORY.load("sprites/items/strawberry.png", icon_height)
        blueberry_icon = SPRITE_FACTORY.load("sprites/items/blueberry.png", icon_height)
        item_icons = {
            "strawberry": strawberry_icon,
            "blueberry": blueberry_icon,
        }
        self.inventory_ui = InventoryUI(
            self.font.get_font(FontSize.MEDIUM, FontStyle.HANDWRITTING), item_icons, self.inputs.layout.right_window
        )

    def _init_gameplay(self):
        self.gravity = ss.game_units_to_decimal(0.001)
        self.sara = Player.load(self.gravity)
        self.hazard = Hazard()
        self.level = Level(self.sara.inventory, LEVEL_1_SPEC)
        self.away = True
        self.colliding_npc: Npc | None = None
        self.particles = []

    # noinspection PyAttributeOutsideInit
    def run(self):
        while self.inputs.running:
            try:
                dt = self.clock.tick_busy_loop(self.FPS)
                self.fps_counter.update(dt)
                self.inputs.process_inputs()
                if self.inputs.in_menu:
                    self.music.play("sounds/music/Fruit World.mp3")
                    self.inputs.main_menu.draw(self.inputs.screen)
                elif self.inputs.is_game_over:
                    self.level.draw_level(self.inputs.game_surface, self.sara)
                    self.game_over_screen.draw()

                else:
                    self.music.play(self.level.music_path)
                    now_ms = pygame.time.get_ticks()
                    self.dialog_vm.handle_event(self.inputs.is_pick_pressed, self.inputs.is_exit_pressed, self.away, now_ms, dt)

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

                    self.dialog_vm.update(dt)

                    self.hazard.update(dt)
                    self.hazard.collide_hazard(self.level.current_map.hazard, self.sara.player_rect, self.sara.health)
                    if self.sara.health.restart_game:
                        self.inputs.is_game_over = True
                    all_solids = self.level.current_map.platforms + self.level.current_map.hazard
                    self.sara.process_inputs(dt, self.inputs, all_solids)
                    self.level.change_map(self.sara)
                    self.sara.update_sprite(self.inputs, dt)

                    collected_pos = collect_consumables(
                        self.sara.player_rect, self.level.current_map.consumable_objects, self.sara.money, self.sara.health, self.sara.mana
                    )
                    for pos in collected_pos:
                        self.particles.extend(Particle.spawn_particles(pos))
                    self.sunlight.update(dt)
                    self.level.update_level(now_ms)
                    self.inputs.screen.fill((53, 71, 46))
                    self.level.draw_level(self.inputs.game_surface, self.sara)
                    self.particles = Particle.create_blink_effect(self.inputs.game_surface, self.particles, dt)
                    self.sunlight.draw(self.inputs.game_surface)
                    self.lighting.reset()
                    # self.lighting.draw_light(self.sara.player_rect.center)
                    self.lighting.apply(self.inputs.game_surface)
                    if self.inputs.DEBUG_OVERLAYS:
                        self.level.draw_debug(self.inputs.game_surface, [self.sara])

                    self.inputs.screen.blit(self.inputs.game_surface, self.inputs.layout.game_view.topleft)
                    self.inputs.layout.draw_panel(self.inputs.screen)
                    self.inputs.layout.draw_panel_windows(self.inputs.screen)
                    # DIALOG:
                    self.dialog_view.draw(self.inputs.screen, self.dialog_vm)
                    # PRZEDMIOTY:

                    if self.inputs.is_pick_pressed:
                        for bush in itertools.chain(self.level.current_map.strawberry_bushes, self.level.current_map.blueberry_bushes):
                            picked_items = bush.try_pick_berries(self.sara.player_rect)
                            if picked_items > 0:
                                self.sara.inventory.add(bush.berry_item_id, picked_items)

                    self.inventory_ui.draw(self.inputs.screen, self.sara.inventory)
                    self.resources_ui.draw(self.inputs.screen, self.sara.money, self.sara.health, self.sara.mana)

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
