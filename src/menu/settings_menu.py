import pygame

from menu.ui import Action, Button, Modal, UIManager
from screen import scale_screen as ss
from screen.game_units import GameUnit


class GameSettings:
    def __init__(self, font: pygame.font.Font):
        w = ss.GAME_WIDTH
        h = ss.GAME_HEIGHT
        self.modal_w, self.modal_h = w // 2, h // 1.6
        self.pad = GameUnit(24).pixels
        self.btn_w = (self.modal_w - self.pad * 3) // 2
        self.btn_h = GameUnit(56).pixels
        self.rect = pygame.Rect(0, 0, self.modal_w, self.modal_h)
        self.rect.center = (w // 2, h // 2)  # makes rect in center
        self._color = 80, 100, 75
        self.font = font
        self.ui = UIManager()
        self.make_settings_modal()

    def make_settings_modal(self):
        pad = GameUnit(25).pixels
        btn_h = GameUnit(60).pixels
        buttons = [
            Button(self._slot(0, 0), "UNAVAILABLE", Action.RES_800x600, self.font),
            Button(self._slot(1, 0), "UNAVAILABLE", Action.RES_1280x720, self.font),
            Button(self._slot(0, 1), "RESTART LEVEL", Action.RESET_LEVEL, self.font),
            Button(self._slot(1, 1), "MAIN MENU", Action.GO_TO_MENU, self.font),
            Button(
                pygame.Rect(self.rect.centerx - GameUnit(90).pixels, self.rect.bottom - btn_h - 2 * pad, GameUnit(200).pixels, btn_h),
                "Return",
                Action.CLOSE_WINDOW,
                self.font,
            ),
        ]
        modal = Modal(pygame.Rect(0, 0, 0, 0), "", buttons, self.font)
        self.ui.push(modal)

    def _slot(self, col: int, row: int) -> pygame.Rect:
        x = self.rect.left + self.pad + col * (self.btn_w + self.pad)
        y = self.rect.top + GameUnit(200).pixels + row * (self.btn_h + self.pad)
        return pygame.Rect(x, y, self.btn_w, self.btn_h)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._color, self.rect, border_radius=GameUnit(30).pixels)
        text_surface = self.font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(text_surface, (self.modal_w - GameUnit(30).pixels, self.modal_h - GameUnit(400).pixels))
        self.ui.draw(screen)
        shadow_rect = self.rect.inflate(3, 3).move(2, 2)
        pygame.draw.rect(screen, (65, 85, 60), shadow_rect, width=GameUnit(5).non_zero_pixels, border_radius=GameUnit(30).pixels)
        pygame.draw.rect(screen, (140, 165, 135), self.rect, width=GameUnit(5).non_zero_pixels, border_radius=GameUnit(30).pixels)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self.ui.handle_event(event)


def toggle_settings(self, ui: UIManager, screen: pygame.Surface, font: pygame.font.Font):
    if ui.active:
        ui.pop()
    else:
        ui.push(self.make_settings_modal(screen.get_size(), font))
