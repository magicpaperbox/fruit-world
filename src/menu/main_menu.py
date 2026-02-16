import pygame

import screen.scale_screen as ss
from menu.ui import Action, Button, Modal, UIManager
from render.sprite_factory import SPRITE_FACTORY
from screen.game_units import GameUnit


class MainMenu:
    def __init__(self, screen_size: tuple[int, int], font: pygame.font.Font):
        self.screen_size = screen_size
        self.font = font
        self.ui = UIManager()
        self._rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.background = SPRITE_FACTORY.load("sprites/map/main_menu.png", ss.SCREEN_HEIGHT)
        self._setup()

    def _setup(self):
        cx, cy = self._rect.center

        buttons = [
            Button(
                rect=pygame.Rect(
                    cx - GameUnit(173).pixels,
                    cy + GameUnit(190).pixels,
                    GameUnit(330).pixels,
                    GameUnit(70).pixels,
                ),
                text="",
                action=Action.START_GAME,
                font=self.font,
            ),
            Button(
                rect=pygame.Rect(
                    cx - GameUnit(167).pixels,
                    cy + GameUnit(430).pixels,
                    GameUnit(315).pixels,
                    GameUnit(55).pixels,
                ),
                text="",
                action=Action.QUIT_GAME,
                font=self.font,
            ),
        ]

        modal = Modal(pygame.Rect(self._rect), "", GameUnit(50).pixels, buttons, self.font, transparent_background=True)
        self.ui.push(modal)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        self.ui.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self.ui.handle_event(event)
