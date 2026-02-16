import pygame

from menu.ui import Action, Button, Modal, UIManager
from render.drawable import Drawable
from screen.game_units import GameUnit


class GameOverScreen(Drawable):
    def __init__(self, font: pygame.font.Font):
        self._font = font
        self._rect = pygame.Rect(0, 0, GameUnit(500).pixels, GameUnit(300).pixels)
        self._ui = UIManager()
        self._setup()

    def draw(self, screen: pygame.surface.Surface):
        self._ui.draw(screen)

    def _setup(self):
        cx, cy = self._rect.center

        button_y = cy + GameUnit(60).pixels
        button_width = GameUnit(180).pixels
        button_height = GameUnit(50).pixels
        gap = GameUnit(40).pixels
        buttons = [
            Button(
                rect=pygame.Rect(
                    cx - button_width - gap // 2,
                    button_y,
                    button_width,
                    button_height,
                ),
                text="RESTART",
                action=Action.RESET_LEVEL,
                font=self._font,
                transparency=120,
            ),
            Button(
                rect=pygame.Rect(
                    cx + gap // 2,
                    button_y,
                    button_width,
                    button_height,
                ),
                text="MENU",
                action=Action.GO_TO_MENU,
                font=self._font,
                transparency=120,
            ),
        ]

        modal = Modal(pygame.Rect(self._rect), "GAME OVER", GameUnit(40).pixels, buttons, self._font)
        self._ui.push(modal)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self._ui.handle_event(event)
