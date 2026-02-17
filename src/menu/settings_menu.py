import pygame

from menu.ui.actions import Action
from menu.ui.modal import Modal
from menu.ui.ui_manager import UIManager
from menu.ui.widgets import Button, Slider
from screen.game_units import GameUnit


class GameSettings:
    def __init__(self, font: pygame.font.Font, change_volume_callback):
        self._modal_w, self._modal_h = GameUnit(1000).pixels, GameUnit(700).pixels
        self._rect = pygame.Rect(0, 0, self._modal_w, self._modal_h)
        self._pad = GameUnit(40).pixels
        self._btn_w = (self._modal_w - self._pad * 3) // 2
        self._btn_h = GameUnit(56).pixels
        self.change_volume_callback = change_volume_callback
        self._font = font
        self._ui = UIManager()
        self._setup()

    def _setup(self):
        buttons = [
            Button(self._slot(0, 0), "UNAVAILABLE", Action.RES_800x600, self._font, transparency=120),
            Button(self._slot(1, 0), "UNAVAILABLE", Action.RES_1280x720, self._font, transparency=120),
            Button(self._slot(0, 1), "RESTART LEVEL", Action.RESET_LEVEL, self._font, transparency=120),
            Button(self._slot(1, 1), "MAIN MENU", Action.GO_TO_MENU, self._font, transparency=120),
            Button(
                pygame.Rect(
                    self._rect.centerx - GameUnit(90).pixels,
                    self._rect.bottom - self._btn_h - 2 * self._pad,
                    GameUnit(200).pixels,
                    self._btn_h,
                ),
                "Return",
                Action.CLOSE_WINDOW,
                self._font,
                transparency=180,
            ),
            Slider(self._slot(0, 2), Action.NONE, on_change=self.change_volume_callback),
        ]

        modal = Modal(pygame.Rect(self._rect), "SETTINGS", GameUnit(250).pixels, buttons, self._font)
        self._ui.push(modal)

    def _slot(self, col: int, row: int) -> pygame.Rect:
        x = self._rect.left + self._pad + col * (self._btn_w + self._pad)
        y = self._rect.top + GameUnit(200).pixels + row * (self._btn_h + self._pad)
        return pygame.Rect(x, y, self._btn_w, self._btn_h)

    def draw(self, screen: pygame.Surface):
        self._ui.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self._ui.handle_event(event)


# def toggle_settings(self, ui: UIManager, screen: pygame.Surface, font: pygame.font.Font):
#     if ui.active:
#         ui.pop()
#     else:
#         ui.push(self._setup(screen.get_size(), font))
