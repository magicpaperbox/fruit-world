import pygame

from scale_screen import GAME_HEIGHT


class Layout:
    def __init__(
        self,
        screen_w: int,
        screen_h: int,
        game_w: int,
        *,
        pad: int = 6,
        gap: int = 10,
    ):
        self.screen = pygame.Rect(0, 0, screen_w, screen_h)

        self.side_w = max(0, (screen_w - game_w) // 2)
        game_top = 0
        game_height = GAME_HEIGHT
        self.left_panel = pygame.Rect(0, game_top, self.side_w, game_height)
        self.game_view = pygame.Rect(self.side_w, game_top, game_w, game_height)
        self.right_panel = pygame.Rect(self.side_w + game_w, game_top, self.side_w, game_height)

        self.pad = pad
        self.gap = gap
        self.left_window = self._inner_rect(self.left_panel)
        self.right_window = self._inner_rect(self.right_panel)



    def _inner_rect(self, panel: pygame.Rect) -> pygame.Rect:
        return panel.inflate(-2 * self.pad, -2 * self.pad)

    def draw_panels(self, screen: pygame.Surface):
        # tło paneli bocznych (oddzielne od świata gry)
        panel_bg = (45, 65, 45)
        screen.fill(panel_bg, self.left_panel)
        screen.fill(panel_bg, self.right_panel)

        # separatory (linie od góry do dołu)
        sep = (25, 35, 25)
        pygame.draw.line(screen, sep, self.game_view.topleft, self.game_view.bottomleft, 2)
        pygame.draw.line(screen, sep, self.game_view.topright, self.game_view.bottomright, 2)

    def draw_panel_windows(self, screen: pygame.Surface):
        fill = (80, 100, 75)
        stroke = (140, 165, 135)

        for r in (self.left_window, self.right_window):
            pygame.draw.rect(screen, fill, r, border_radius=10)
            pygame.draw.rect(screen, stroke, r, width=2, border_radius=10)