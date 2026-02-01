from typing import Protocol

import pygame


class Debuggable(Protocol):
    def draw_debug(self, screen: pygame.surface.Surface):
        pass
