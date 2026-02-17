import pygame

from menu.ui.actions import Action
from screen.game_units import GameUnit


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
