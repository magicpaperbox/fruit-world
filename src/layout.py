import pygame

import scale_screen as ss


class Layout:
    def __init__(self, pad: int, gap: int):
        self.screen = pygame.Rect(0, 0, ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT)

        game_top = 0
        self.game_view = pygame.Rect(0, game_top, ss.GAME_WIDTH, ss.GAME_HEIGHT)

        self.right_panel = pygame.Rect(
            self.game_view.right,
            game_top,
            ss.SCREEN_WIDTH - self.game_view.right,
            ss.GAME_HEIGHT,
        )

        self.pad = pad
        self.gap = gap
        self.right_window = self._inner_rect(self.right_panel)



    def _inner_rect(self, panel: pygame.Rect) -> pygame.Rect:
        return panel.inflate(-3 * self.pad, -3 * self.pad)

    def draw_panel(self, screen: pygame.Surface):
        # tło panelu
        fill = (80, 100, 75)
        screen.fill(fill, self.right_panel)

        # bevel (jak w dialogu): góra/lewo jaśniej, dół/prawo ciemniej
        light = (140, 165, 135)
        dark = (65, 85, 60)

        r = self.right_panel
        pygame.draw.line(screen, light, r.topleft, (r.right - 1, r.top), 2)
        pygame.draw.line(screen, light, r.topleft, (r.left, r.bottom - 1), 2)
        pygame.draw.line(screen, dark, (r.left, r.bottom - 1), (r.right - 1, r.bottom - 1), 2)
        pygame.draw.line(screen, dark, (r.right - 1, r.top), (r.right - 1, r.bottom - 1), 2)

    def draw_panel_windows(self, screen: pygame.Surface):
        fill = (80, 100, 75)
        light = (140, 165, 135)
        dark = (65, 85, 60)

        r = self.right_window

        # tło
        pygame.draw.rect(screen, fill, r, border_radius=10)

        # jasny obrys
        pygame.draw.rect(screen, light, r, width=2, border_radius=10)

        # cień
        shadow_rect = r.inflate(2, 2).move(1, 1)
        pygame.draw.rect(screen, dark, shadow_rect, width=2, border_radius=10)

