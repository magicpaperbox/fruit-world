import pygame

from screen import scale_screen as ss
from screen.game_units import GameUnit


class Layout:
    def __init__(self):
        game_top = 0
        self.game_view = pygame.Rect(0, game_top, ss.GAME_WIDTH, ss.GAME_HEIGHT)

        self._right_panel = pygame.Rect(
            self.game_view.right,
            game_top,
            ss.SCREEN_WIDTH - self.game_view.right,
            ss.GAME_HEIGHT,
        )

        self._pad = GameUnit(-18).pixels
        self._gap = GameUnit(6).pixels
        self.right_window = self._inner_rect(self._right_panel)
        self._border = ss.game_units_to_px_min(3)
        self._fill_rgb = (80, 100, 75)
        self._light_rgb = (140, 165, 135)
        self._dark_rgb = (65, 85, 60)

    def _inner_rect(self, panel: pygame.Rect) -> pygame.Rect:
        return panel.inflate(self._pad, self._pad)

    def draw_panel(self, screen: pygame.Surface):
        screen.fill(self._fill_rgb, self._right_panel)

        r = self._right_panel
        pygame.draw.line(screen, self._light_rgb, r.topleft, (r.right - 1, r.top), self._border)
        pygame.draw.line(screen, self._light_rgb, r.topleft, (r.left, r.bottom - 1), self._border)
        pygame.draw.line(screen, self._dark_rgb, (r.left, r.bottom - 1), (r.right - 1, r.bottom - 1), self._border)
        pygame.draw.line(screen, self._dark_rgb, (r.right - 1, r.top), (r.right - 1, r.bottom - 1), self._border)

    def draw_panel_windows(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._fill_rgb, self.right_window, border_radius=GameUnit(35).pixels)
        pygame.draw.rect(screen, self._light_rgb, self.right_window, width=self._border, border_radius=GameUnit(15).pixels)
        shadow_rect = self.right_window.inflate(self._border, self._border).move(1, 1)
        pygame.draw.rect(screen, self._dark_rgb, shadow_rect, width=self._border, border_radius=GameUnit(15).pixels)
