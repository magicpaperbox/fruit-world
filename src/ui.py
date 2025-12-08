import pygame
from enum import Enum, auto


class Action(Enum):
    NONE = auto()
    CLOSE_MENU = auto()
    QUIT_GAME = auto()
    RESET_LEVEL = auto()
    RES_800x600 = auto()
    RES_1280x720 = auto()

class Button:
    def __init__(
            self,
            rect: pygame.Rect,
            text: str,
            action: Action,
            font: pygame.font.Font
    ):
        self.rect = rect
        self.text = text
        self.action = action
        self.font = font
        self._pressed = False
        self._hover = False


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
        bg = (70, 70, 80)
        if self._hover:
            bg = (90, 90, 110)
        if self._pressed:
            bg = (60, 60, 75)
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, (200, 200, 220), self.rect, 2, border_radius=8)
        txt = self.font.render(self.text, True, (240, 240, 255))
        surf.blit(txt, txt.get_rect(center=self.rect.center))

class Modal:
    def __init__(self, rect: pygame.Rect, title: str, buttons: list[Button], font: pygame.font.Font):
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
        overlay.fill((0, 0, 0, 140))
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
            self.modals.p

    def handle_event(self, e: pygame.event.Event) -> Action:
        if self.modals:
            return self.modals[-1].handle_event(e)
        return Action.NONE

    def draw(self, surf: pygame.Surface):
        for m in self.modals:
            m.draw(surf)