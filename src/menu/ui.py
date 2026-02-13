from enum import Enum, auto

import pygame


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
        buttons: list[Button],
        font: pygame.font.Font,
    ):
        self.rect = rect
        self.title = title
        self.buttons = buttons
        self.font = font

    def handle_event(self, e: pygame.event.Event) -> Action:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return Action.CLOSE_MENU
        for b in self.buttons:
            a = b.handle_event(e)
            if a is not Action.NONE:
                return a
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        overlay = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        surf.blit(overlay, (0, 0))

        pygame.draw.rect(surf, (30, 30, 40), self.rect, border_radius=16)
        pygame.draw.rect(surf, (220, 220, 235), self.rect, 2, border_radius=16)

        title_s = self.font.render(self.title, True, (255, 255, 255))
        surf.blit(title_s, title_s.get_rect(midtop=(self.rect.centerx, self.rect.top + 16)))

        for b in self.buttons:
            b.draw(surf)


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
