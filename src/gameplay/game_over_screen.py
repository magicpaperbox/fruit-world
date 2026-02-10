import pygame

from menu.ui import Action, Button, Modal, UIManager
from render.drawable import Drawable
from screen import scale_screen as ss
from screen.game_units import GameUnit


class GameOverScreen(Drawable):
    def __init__(self, font: pygame.font.Font):
        self._font = font

        game_width = ss.GAME_WIDTH
        game_height = ss.GAME_HEIGHT
        self._rect = pygame.Rect(0, 0, 500, 300)
        self._rect.center = (game_width // 2, game_height // 2)
        self._color = 80, 100, 75
        self._ui = UIManager()
        self._setup()

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, self._color, self._rect, border_radius=30)
        text_surface = self._font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self._rect.centerx
        text_rect.centery = self._rect.centery - text_rect.height

        screen.blit(text_surface, text_rect)
        self._ui.draw(screen)

        shadow_rect = self._rect.inflate(3, 3).move(2, 2)
        pygame.draw.rect(screen, (65, 85, 60), shadow_rect, width=ss.game_units_to_px_min(6), border_radius=30)
        pygame.draw.rect(screen, (140, 165, 135), self._rect, width=ss.game_units_to_px_min(6), border_radius=30)

    def _setup(self):
        cx, cy = self._rect.center

        button_y = cy + GameUnit(80).pixels
        button_width = GameUnit(180).pixels
        button_height = GameUnit(50).pixels
        gap = GameUnit(60).pixels
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

        modal = Modal(pygame.Rect(0, 0, 0, 0), "", buttons, self._font)
        self._ui.push(modal)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self._ui.handle_event(event)
