import pygame

from screen import scale_screen as ss
from screen.layout import Layout


class Control:
    def __init__(self, game_surface, screen, layout, fullscreen, dialog_vm, jump_sound):
        self.game_surface = game_surface
        self.screen = screen
        self.layout = layout
        self.fullscreen = fullscreen
        self.dialog_vm = dialog_vm
        self.space_down_this_frame = False
        self.is_pick_pressed = False
        self.is_exit_pressed = False
        self.settings_pressed = False
        self.running = True
        self.DEBUG_OVERLAYS = False
        self.is_right_pressed = False
        self.is_left_pressed = False
        self.jump_sound = jump_sound

    def keyboard_roles(self, dt, now_ms, away):
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
                self.layout = Layout(16, 16)
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
        self.dialog_vm.handle_event(self.is_pick_pressed, self.is_exit_pressed, away, now_ms, dt)
        keys = pygame.key.get_pressed()
        self.is_right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        self.is_left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]
