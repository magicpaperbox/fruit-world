from typing import Protocol

import pygame


class Drawable(Protocol):
    def draw(self, screen: pygame.surface.Surface):
        pass
