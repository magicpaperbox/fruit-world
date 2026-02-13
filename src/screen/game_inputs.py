import pygame

from menu.ui import Action
from screen import scale_screen as ss
from screen.layout import Layout


class GameInputs:
    def __init__(self, game_surface, screen, layout, fullscreen, jump_sound, main_menu, game_over, gameplay_settings_screen):
        self.game_surface = game_surface
        self.screen = screen
        self.layout = layout
        self.fullscreen = fullscreen
        self.is_interaction_pressed = False
        self.is_exit_pressed = False
        self.settings_pressed = False
        self.game_loop_running = True
        self.DEBUG_OVERLAYS = False
        self._is_right_pressed = False
        self._is_left_pressed = False
        self._jump_sound = jump_sound
        self._space_pressed_this_frame = False
        self.in_menu = True
        self.main_menu = main_menu
        self.in_settings = False
        self.gameplay_settings_screen = gameplay_settings_screen
        self.is_game_over = False
        self.game_over_screen = game_over
        self.reset_level = False
        self._allow_movement = True

    def block_movement(self):
        self._allow_movement = False

    def unblock_movement(self):
        self._allow_movement = True

    @property
    def is_right_pressed(self):
        return self._is_right_pressed if self._allow_movement else False

    @property
    def is_left_pressed(self):
        return self._is_left_pressed if self._allow_movement else False

    @property
    def space_pressed_this_frame(self):
        return self._space_pressed_this_frame if self._allow_movement else False

    def process_inputs(self):
        self._space_pressed_this_frame = False
        self.is_interaction_pressed = False
        self.is_exit_pressed = False
        self.settings_pressed = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.game_loop_running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                self.screen = ss.init_display(ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT, self.fullscreen)
                self.layout = Layout()
                self.game_surface = pygame.Surface((ss.GAME_WIDTH, ss.GAME_HEIGHT)).convert()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self._space_pressed_this_frame = True
                self._jump_sound.play()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
                self.is_interaction_pressed = True
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
                    self.game_loop_running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.in_menu = True

            if self.settings_pressed and not self.in_settings:
                self.in_settings = True
            elif self.settings_pressed and self.in_settings:
                self.in_settings = False

            if self.in_settings:
                action = self.gameplay_settings_screen.handle_event(e)
                if action == Action.RESET_LEVEL:
                    self.is_game_over = False
                    self.reset_level = True
                    self.in_settings = False
                elif action == Action.GO_TO_MENU:
                    self.is_game_over = False
                    self.in_menu = True
                    self.reset_level = True
                    self.in_settings = False
                elif action == Action.CLOSE_WINDOW:
                    self.in_settings = False

            if self.is_game_over:
                action = self.game_over_screen.handle_event(e)

                if action == Action.RESET_LEVEL:
                    self.is_game_over = False
                    self.reset_level = True
                elif action == Action.GO_TO_MENU:
                    self.is_game_over = False
                    self.in_menu = True
                    self.reset_level = True
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.in_menu = True

        keys = pygame.key.get_pressed()
        self._is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        self._is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]
