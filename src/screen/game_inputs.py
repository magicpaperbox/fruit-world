import pygame

from menu.ui import Action
from screen import scale_screen as ss
from screen.layout import Layout


class GameInputs:
    def __init__(self, game_surface, screen, layout, fullscreen, jump_sound, main_menu, game_over):
        self.game_surface = game_surface
        self.screen = screen
        self.layout = layout
        self.fullscreen = fullscreen
        self.space_down_this_frame = False
        self.is_pick_pressed = False
        self.is_exit_pressed = False
        self.settings_pressed = False
        self.running = True
        self.DEBUG_OVERLAYS = False
        self.is_right_pressed = False
        self.is_left_pressed = False
        self.jump_sound = jump_sound
        self.in_menu = True
        self.main_menu = main_menu
        self.is_game_over = False
        self.game_over_screen = game_over

    def process_inputs(self):
        self.space_down_this_frame = False
        self.is_pick_pressed = False
        self.is_exit_pressed = False
        self.settings_pressed = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                self.screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, self.fullscreen)
                self.layout = Layout()
                self.game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.space_down_this_frame = True
                self.jump_sound.play()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                self.is_pick_pressed = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_0:
                self.DEBUG_OVERLAYS = not self.DEBUG_OVERLAYS
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                self.is_exit_pressed = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                self.settings_pressed = True

            if self.in_menu:
                action = self.main_menu.handle_event(e)

                if action == Action.START_GAME:
                    self.in_menu = False
                elif action == Action.QUIT_GAME:
                    self.running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.in_menu = True

            if self.is_game_over:
                action = self.game_over_screen.handle_event(e)

                if action == Action.RESET_LEVEL:
                    self.is_game_over = False
                    print("Zresetuj grę ręcznie")
                elif action == Action.GO_TO_MENU:
                    self.in_menu = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.in_menu = True

        keys = pygame.key.get_pressed()
        self.is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        self.is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]
