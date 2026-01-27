import pygame

import screen.scale_screen as ss
from menu.ui import Action, Button, Modal, UIManager
from render.sprite_factory import SPRITE_FACTORY


class MainMenu:
    def __init__(self, screen_size: tuple[int, int], font: pygame.font.Font):
        self.screen_size = screen_size
        self.font = font
        self.ui = UIManager()
        self.background = SPRITE_FACTORY.load("sprites/map/main_menu.png", ss.SCREEN_HEIGHT)
        self._setup()

    def _setup(self):
        w, h = self.screen_size
        cx, cy = w // 2, h // 2

        buttons = [
            Button(
                rect=pygame.Rect(
                    cx - ss.game_units_to_px(164),
                    cy + ss.game_units_to_px(190),
                    ss.game_units_to_px(330),
                    ss.game_units_to_px(70),
                ),
                text="Graj",
                action=Action.START_GAME,
                font=self.font,
            ),
            Button(
                rect=pygame.Rect(
                    cx - ss.game_units_to_px(158),
                    cy + ss.game_units_to_px(430),
                    ss.game_units_to_px(315),
                    ss.game_units_to_px(55),
                ),
                text="Wyjdź",
                action=Action.QUIT_GAME,
                font=self.font,
            ),
        ]

        modal = Modal(pygame.Rect(0, 0, 0, 0), "", buttons, self.font)
        self.ui.push(modal)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        self.ui.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self.ui.handle_event(event)
