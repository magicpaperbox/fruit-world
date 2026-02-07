import pygame

from menu.ui import Action, Button, Modal, UIManager
from screen import scale_screen as ss


class GameOverScreen:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font

        game_width = ss.GAME_WIDTH
        game_height = ss.GAME_HEIGHT
        self._rect = pygame.Rect(0, 0, 500, 300)
        self._rect.center = (game_width // 2, game_height // 2)
        self._color = 30, 90, 40
        self.ui = UIManager()
        self._setup()

    def draw(self):
        pygame.draw.rect(self.screen, self._color, self._rect, border_radius=30)
        text_surface = self.font.render("Game Over", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self._rect.centerx
        text_rect.top = self._rect.top + 20
        self.screen.blit(text_surface, text_rect)
        self.ui.draw(self.screen)

    def _setup(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        cx, cy = w // 2, h // 2

        button_y = cy + 80
        button_width = 150
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
                font=self.font,
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
                font=self.font,
            ),
        ]

        modal = Modal(pygame.Rect(0, 0, 0, 0), "", buttons, self.font)
        self.ui.push(modal)

    def handle_event(self, event: pygame.event.Event) -> Action:
        return self.ui.handle_event(event)
