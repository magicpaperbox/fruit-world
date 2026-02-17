import pygame

from menu.ui.actions import Action
from menu.ui.modal import Modal


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
