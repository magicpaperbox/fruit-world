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
        self._color = 140, 180, 130
        self._ui = UIManager()
        self._setup()

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, self._color, self._rect, border_radius=30)
        text_surface = self._font.render("Game Over", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self._rect.centerx
        text_rect.top = self._rect.top + 20
        screen.blit(text_surface, text_rect)
        self._ui.draw(screen)

    def _setup(self):
        cx, cy = self._rect.center

        button_y = cy + 80
        button_width = GameUnit(150).pixels
        button_height = 50
        gap = 20
        buttons = [
            Button(
                rect=pygame.Rect(
                    cx - button_width - gap // 2,
                    button_y,
                    button_width,
                    button_height,
                ),
                text="Restart",
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
                text="Menu",
                action=Action.GO_TO_MENU,
                font=self._font,
                transparency=120,
            ),
        ]

        modal = Modal(pygame.Rect(0, 0, 0, 0), "", buttons, self._font)
        self._ui.push(modal)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self._ui.handle_event(event)
