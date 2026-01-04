import pygame
from ui import UIManager, Modal, Button, Action


def make_settings_modal(screen_size: tuple[int, int], font: pygame.font.Font) -> Modal:
    W, H = screen_size
    modal_w, modal_h = int(W * 0.5), int(H * 0.6)
    rect = pygame.Rect(0, 0, modal_w, modal_h)
    rect.center = (W // 2, H // 2)

    pad = 24
    btn_w = (modal_w - pad * 3) // 2
    btn_h = 56

    def slot(col: int, row: int) -> pygame.Rect:
        x = rect.left + pad + col * (btn_w + pad)
        y = rect.top + 80 + row * (btn_h + pad)
        return pygame.Rect(x, y, btn_w, btn_h)

    buttons = [
        Button(slot(0, 0), "Rozdzielczość 800×600", Action.RES_800x600, font),
        Button(slot(1, 0), "Rozdzielczość 1280×720", Action.RES_1280x720, font),
        Button(slot(0, 1), "Reset poziomu", Action.RESET_LEVEL, font),
        Button(slot(1, 1), "Wyjdź z gry", Action.QUIT_GAME, font),
        Button(
            pygame.Rect(rect.centerx - 90, rect.bottom - btn_h - pad, 180, btn_h),
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
