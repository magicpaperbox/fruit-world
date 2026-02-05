from enum import Enum

import pygame

from screen import scale_screen


class FontSize(Enum):
    SMALL = 8
    MEDIUM = 9
    LARGE = 10
    XLARGE = 14


class FontStyle(Enum):
    CAPS_CONDENSED = "sprites/fonts/AmaticSC.ttf"
    CAPS_CONDENSED_BOLD = "sprites/fonts/AmaticSC-Bold.ttf"
    ORNATE = "sprites/fonts/Delius.ttf"
    SIMPLE = "sprites/fonts/Fredoka.ttf"
    HANDWRITTING = "sprites/fonts/LaBelleAurore.ttf"
    RUSTIC = "sprites/fonts/PrincessSofia.ttf"


class FontsFactory:
    def __init__(self):
        self._resolution_size = scale_screen.get_resolution()

    def get_font(self, font_size: FontSize, font_style: FontStyle):
        scale = self._resolution_size + 3
        size = font_size.value + scale
        return pygame.font.Font(font_style.value, size)
