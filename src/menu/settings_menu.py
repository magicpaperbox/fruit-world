import pygame
from ui import Action, Button, Modal, UIManager

from screen.game_units import GameUnit


def make_settings_modal(screen_size: tuple[int, int], font: pygame.font.Font) -> Modal:
    w, h = screen_size
    modal_w, modal_h = int(w * 0.5), int(h * 0.6)
    rect = pygame.Rect(0, 0, modal_w, modal_h)
    rect.center = (w // 2, h // 2)

    pad = GameUnit(24).pixels
    btn_w = (modal_w - pad * 3) // 2
    btn_h = GameUnit(56).pixels

    def slot(col: int, row: int) -> pygame.Rect:
        x = rect.left + pad + col * (btn_w + pad)
        y = rect.top + GameUnit(80).pixels + row * (btn_h + pad)
        return pygame.Rect(x, y, btn_w, btn_h)

    buttons = [
        Button(slot(0, 0), "Rozdzielczość 800×600", Action.RES_800x600, font),
        Button(slot(1, 0), "Rozdzielczość 1280×720", Action.RES_1280x720, font),
        Button(slot(0, 1), "Reset poziomu", Action.RESET_LEVEL, font),
        Button(slot(1, 1), "Wyjdź z gry", Action.QUIT_GAME, font),
        Button(
            pygame.Rect(rect.centerx - GameUnit(90).pixels, rect.bottom - btn_h - pad, GameUnit(180).pixels, btn_h),
            "Wróć do gry",
            Action.CLOSE_MENU,
            font,
        ),
    ]
    return Modal(rect, "Ustawienia", buttons, font)


def toggle_settings(ui: UIManager, screen: pygame.Surface, font: pygame.font.Font):
    if ui.active:
        ui.pop()
    else:
        ui.push(make_settings_modal(screen.get_size(), font))
