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
    CHANGE_VOL = auto()


class Button:
    def __init__(self, rect: pygame.Rect, text: str, action: Action, font: pygame.font.Font, transparency=0):
        self.rect = rect
        self._text = text
        self._action = action
        self._font = font
        self._pressed = False
        self._hover = False
        self._transparency = transparency

    def handle_event(self, e: pygame.event.Event) -> Action:
        if e.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(e.pos)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self._pressed = True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if self._pressed and self.rect.collidepoint(e.pos):
                self._pressed = False
                return self._action
            self._pressed = False
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        bg = (70, 70, 80, self._transparency)
        if self._hover:
            bg = (230, 200, 100, 20)
        if self._pressed:
            bg = (0, 0, 0, 50)
        temp_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        temp_surface = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, bg, temp_rect, border_radius=15)
        surf.blit(temp_surface, self.rect.topleft)
        text_surface = self._font.render(self._text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surf.blit(text_surface, text_rect)


class Slider:
    def __init__(self, rect: pygame.Rect, action: Action, on_change=None):
        self.rect = rect
        self._min_volume = 0
        self._max_volume = 1
        self.current_volume = 0.5
        self._hover = False
        self._pressed = False
        self._action = action
        self.on_change = on_change

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (65, 85, 60), self.rect, border_radius=GameUnit(30).pixels)
        volume_ratio = self.current_volume
        handle_width = GameUnit(55).pixels
        handle_x = self.rect.x + (self.rect.width - handle_width) * volume_ratio
        handle_y = self.rect.y
        handle_rect = pygame.Rect(handle_x, handle_y, handle_width, self.rect.height)
        color = (180, 200, 170) if self._hover or self._pressed else (160, 170, 150)
        pygame.draw.rect(screen, color, handle_rect, border_radius=GameUnit(70).pixels)

    def handle_event(self, e: pygame.event.Event) -> Action:
        returned_action = Action.NONE
        if e.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(e.pos)
            if self._pressed:
                self._update_volume(e.pos[0])
                returned_action = self._action
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self._pressed = True
                self._update_volume(e.pos[0])
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self._pressed = False

        return returned_action

    def _update_volume(self, mouse_x_pos: int):
        relative_x = mouse_x_pos - self.rect.x  # relative position in slider
        new_volume = relative_x / self.rect.width
        self.current_volume = max(0.0, min(1.0, new_volume))
        if self.on_change:
            self.on_change(self.current_volume)


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
        original_x = self.rect.x
        original_y = self.rect.y

        self.rect.center = (ss.SCREEN_WIDTH // 2, ss.SCREEN_HEIGHT // 2)
        dx = self.rect.x - original_x
        dy = self.rect.y - original_y

        self.title = title
        self.offset_y = offset_y
        self.buttons = buttons
        for button in self.buttons:
            button.rect.move_ip(dx, dy)
        self.font = font
        self.show_border = True
        self.transparent_background = transparent_background
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
        if not self.transparent_background:
            pygame.draw.rect(surf, (80, 100, 75), self.rect, border_radius=self.border_radius)
            if self.show_border:
                shadow_rect = self.rect.inflate(3, 3).move(2, 2)
                pygame.draw.rect(surf, (65, 85, 60), shadow_rect, width=GameUnit(6).non_zero_pixels, border_radius=self.border_radius)
                pygame.draw.rect(surf, (140, 165, 135), self.rect, width=GameUnit(6).non_zero_pixels, border_radius=self.border_radius)

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
