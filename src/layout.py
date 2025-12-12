import pygame
import pygame

import scale_screen as ss


class Layout:
    def __init__(self, *, pad: int = 6, gap: int = 10):
        self.screen = pygame.Rect(0, 0, ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT)

        game_top = 0
        self.game_view = pygame.Rect(0, game_top, ss.GAME_WIDTH, ss.GAME_HEIGHT)

        self.right_panel = pygame.Rect(
            self.game_view.right,
            game_top,
            ss.SIDE_PANEL_W,
            ss.GAME_HEIGHT,
        )

        self.pad = pad
        self.gap = gap
        self.right_window = self._inner_rect(self.right_panel)



    def _inner_rect(self, panel: pygame.Rect) -> pygame.Rect:
        return panel.inflate(-2 * self.pad, -2 * self.pad)

    def draw_panel(self, screen: pygame.Surface):
        # tło panelu
        fill = (80, 100, 75)
        screen.fill(fill, self.right_panel)

        # bevel (jak w dialogu): góra/lewo jaśniej, dół/prawo ciemniej
        light = (140, 165, 135)
        dark = (65, 85, 60)

        r = self.right_panel
        pygame.draw.line(screen, light, r.topleft, r.topright, 2)
        pygame.draw.line(screen, light, r.topleft, r.bottomleft, 2)
        pygame.draw.line(screen, dark, (r.left, r.bottom - 1), (r.right, r.bottom - 1), 2)
        pygame.draw.line(screen, dark, (r.right - 1, r.top), (r.right - 1, r.bottom), 2)

        # separator między grą a panelem (opcjonalnie)
        sep = (25, 35, 25)
        pygame.draw.line(screen, sep, self.game_view.topright, self.game_view.bottomright, 2)

    def draw_panel_windows(self, screen: pygame.Surface):
        fill = (80, 100, 75)
        stroke = (140, 165, 135)

        pygame.draw.rect(screen, fill, self.right_window, border_radius=10)
        pygame.draw.rect(screen, stroke, self.right_window, width=2, border_radius=10)


# from scale_screen import GAME_HEIGHT
#
#
# class Layout:
#     def __init__(
#         self,
#         screen_w: int,
#         screen_h: int,
#         game_w: int,
#         *,
#         pad: int = 6,
#         gap: int = 10,
#     ):
#         self.screen = pygame.Rect(0, 0, screen_w, screen_h)
#
#         self.side_w = screen_w - 1.2*game_w
#         game_top = 0
#         game_height = GAME_HEIGHT
#         self.game_view = pygame.Rect(
#             0,
#             game_top,
#             game_w,
#             game_height
#         )
#         self.right_panel = pygame.Rect(
#             self.game_view.right,
#             game_top,
#             self.side_w,
#             game_height
#         )
#
#         self.pad = pad
#         self.gap = gap
#         self.right_window = self._inner_rect(self.right_panel)
#
#
#
#     def _inner_rect(self, panel: pygame.Rect) -> pygame.Rect:
#         return panel.inflate(-2 * self.pad, -2 * self.pad)
#
#     def draw_panel(self, screen: pygame.Surface):
#         # tło paneli bocznych (oddzielne od świata gry)
#         panel_bg = (45, 65, 45)
#         screen.fill(panel_bg, self.right_panel)
#
#         # separatory (linie od góry do dołu)
#         sep = (25, 35, 25)
#         pygame.draw.line(screen, sep, self.game_view.topleft, self.game_view.bottomleft, 2)
#         pygame.draw.line(screen, sep, self.game_view.topright, self.game_view.bottomright, 2)
#
#     def draw_panel_windows(self, screen: pygame.Surface):
#         fill = (80, 100, 75)
#         stroke = (140, 165, 135)
#
#         pygame.draw.rect(screen, fill, self.right_window, border_radius=10)
#         pygame.draw.rect(screen, stroke, self.right_window, width=2, border_radius=10)