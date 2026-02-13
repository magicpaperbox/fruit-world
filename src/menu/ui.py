from enum import Enum, auto

import pygame

from screen import scale_screen as ss
from screen.game_units import GameUnit


class Action(Enum):
    NONE = auto()
    CLOSE_MENU = auto()
    QUIT_GAME = auto()
    RESET_LEVEL = auto()
    RES_800x600 = auto()
    RES_1280x720 = auto()
    START_GAME = auto()
    GO_TO_MENU = auto()
    CLOSE_WINDOW = auto()


class Button:
    def __init__(self, rect: pygame.Rect, text: str, action: Action, font: pygame.font.Font, transparency=0):
        self.rect = rect
        self.text = text
        self.action = action
        self.font = font
        self._pressed = False
        self._hover = False
        self.transparency = transparency

    def handle_event(self, e: pygame.event.Event) -> Action:
        if e.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(e.pos)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self._pressed = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if self._pressed and self.rect.collidepoint(e.pos):
                self._pressed = False
                return self.action
            self._pressed = False
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        bg = (70, 70, 80, self.transparency)
        if self._hover:
            bg = (230, 200, 100, 20)
        if self._pressed:
            bg = (0, 0, 0, 50)
        temp_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        temp_surface = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, bg, temp_rect, border_radius=15)
        surf.blit(temp_surface, self.rect.topleft)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surf.blit(text_surface, text_rect)


class Modal:
    def __init__(
        self,
        rect: pygame.Rect,
        title: str,
        offset_y: int,
        buttons: list[Button],
        font: pygame.font.Font,
    ):
        self.rect = rect
        self.title = title
        self.offset_y = offset_y
        self.buttons = buttons
        self.font = font
        self.show_border = True
        self._overlay_alpha = 0
        self.border_radius = GameUnit(30).pixels
        self.vignette = self._make_vignette()

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

        pygame.draw.rect(surf, (80, 100, 75), self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surf, (220, 220, 235), self.rect, 2, border_radius=self.border_radius)

        if self.title:
            title = self.font.render(self.title, True, (255, 255, 255))
            title_y = self.rect.centery - self.offset_y
            title_rect = title.get_rect(centerx=self.rect.centerx, centery=title_y)
            surf.blit(title, title_rect)

        for b in self.buttons:
            b.draw(surf)
        if self.show_border:
            shadow_rect = self.rect.inflate(3, 3).move(2, 2)
            pygame.draw.rect(surf, (65, 85, 60), shadow_rect, width=GameUnit(6).non_zero_pixels, border_radius=self.border_radius)
            pygame.draw.rect(surf, (140, 165, 135), self.rect, width=GameUnit(6).non_zero_pixels, border_radius=self.border_radius)

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


class UIManager:
    def __init__(self):
        self.modals: list[Modal] = []

    @property
    def active(self) -> bool:
        return len(self.modals) > 0

    def push(self, modal: Modal):
        self.modals.append(modal)

    def pop(self):
        if self.modals:
            self.modals.pop()

    def handle_event(self, e: pygame.event.Event) -> Action:
        if self.modals:
            return self.modals[-1].handle_event(e)
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        for m in self.modals:
            m.draw(surf)
