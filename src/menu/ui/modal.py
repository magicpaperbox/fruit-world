import pygame

from menu.ui.actions import Action
from menu.ui.widgets import Button
from screen import scale_screen as ss
from screen.game_units import GameUnit


class Modal:
    def __init__(
        self,
        rect: pygame.Rect,
        title: str,
        offset_y: int,
        buttons: list[Button],
        font: pygame.font.Font,
        transparent_background: bool = False,
    ):
        self.rect = rect
        self.title = title
        self.offset_y = offset_y
        self.buttons = buttons
        self.font = font
        self.transparent_background = transparent_background

        self._border_radius = GameUnit(30).pixels
        self.show_border = True
        self._overlay_alpha = 0

        self._center()
        self.vignette = self._make_vignette()

    def _center(self):
        original_x = self.rect.x
        original_y = self.rect.y
        self.rect.center = (ss.SCREEN_WIDTH // 2, ss.SCREEN_HEIGHT // 2)
        dx = self.rect.x - original_x
        dy = self.rect.y - original_y
        for button in self.buttons:
            button.rect.move_ip(dx, dy)

    def handle_event(self, e: pygame.event.Event) -> Action:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return Action.CLOSE_MENU
        for b in self.buttons:
            a = b.handle_event(e)
            if a is not Action.NONE:
                return a
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        self._overlay_alpha = min(self._overlay_alpha + 5, 220)
        self.vignette.set_alpha(self._overlay_alpha)
        surf.blit(self.vignette, (0, 0))
        if not self.transparent_background:
            pygame.draw.rect(surf, (80, 100, 75), self.rect, border_radius=self._border_radius)
            if self.show_border:
                shadow_rect = self.rect.inflate(3, 3).move(2, 2)
                pygame.draw.rect(surf, (65, 85, 60), shadow_rect, width=GameUnit(6).non_zero_pixels, border_radius=self._border_radius)
                pygame.draw.rect(surf, (140, 165, 135), self.rect, width=GameUnit(6).non_zero_pixels, border_radius=self._border_radius)

        if self.title:
            title = self.font.render(self.title, True, (255, 255, 255))
            title_y = self.rect.centery - self.offset_y
            title_rect = title.get_rect(centerx=self.rect.centerx, centery=title_y)
            surf.blit(title, title_rect)

        for b in self.buttons:
            b.draw(surf)

    @staticmethod
    def _make_vignette():
        width = ss.SCREEN_WIDTH
        height = ss.SCREEN_HEIGHT
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        center = width // 2, height // 2
        max_radius = int((width**2 + height**2) ** 0.5 / 2)
        for r in range(max_radius, 0, -4):
            distance_fraction = r / max_radius
            alpha = int(150 * distance_fraction)
            pygame.draw.circle(overlay, (0, 0, 0, alpha), center, r)
        return overlay
