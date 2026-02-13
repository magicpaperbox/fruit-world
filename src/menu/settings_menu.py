import pygame

from menu.ui import Action, Button, Modal, UIManager
from screen import scale_screen as ss
from screen.game_units import GameUnit


class GameSettings:
    def __init__(self, font: pygame.font.Font):
        game_width = ss.GAME_WIDTH
        game_height = ss.GAME_HEIGHT
        self._modal_w, self._modal_h = game_width // 2, game_height // 1.6
        self._pad = GameUnit(24).pixels
        self._btn_w = (self._modal_w - self._pad * 3) // 2
        self._btn_h = GameUnit(56).pixels
        self._rect = pygame.Rect(0, 0, self._modal_w, self._modal_h)
        self._rect.center = (game_width // 2, game_height // 2)  # makes rect in center
        self._font = font
        self._ui = UIManager()
        self.make_settings_modal()

    def make_settings_modal(self):
        pad = GameUnit(25).pixels
        btn_h = GameUnit(60).pixels
        buttons = [
            Button(self._slot(0, 0), "UNAVAILABLE", Action.RES_800x600, self._font),
            Button(self._slot(1, 0), "UNAVAILABLE", Action.RES_1280x720, self._font),
            Button(self._slot(0, 1), "RESTART LEVEL", Action.RESET_LEVEL, self._font),
            Button(self._slot(1, 1), "MAIN MENU", Action.GO_TO_MENU, self._font),
            Button(
                pygame.Rect(self._rect.centerx - GameUnit(90).pixels, self._rect.bottom - btn_h - 2 * pad, GameUnit(200).pixels, btn_h),
                "Return",
                Action.CLOSE_WINDOW,
                self._font,
            ),
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


def toggle_settings(self, ui: UIManager, screen: pygame.Surface, font: pygame.font.Font):
    if ui.active:
        ui.pop()
    else:
        ui.push(self.make_settings_modal(screen.get_size(), font))
