from enum import Enum

import pygame

from screen import scale_screen as ss


class FontSize(Enum):
    SMALL = 8
    MEDIUM = 9
    LARGE = 10
    XLARGE = 14


class FontStyle(Enum):
    CAPS_CONDENSED = "fonts/AmaticSC.ttf"
    CAPS_CONDENSED_BOLD = "fonts/AmaticSC-Bold.ttf"
    ORNATE = "fonts/Delius.ttf"
    SIMPLE = "fonts/Fredoka.ttf"
    HANDWRITTING = "fonts/LaBelleAurore.ttf"
    RUSTIC = "fonts/PrincessSofia.ttf"


class FontsFactory:
    def __init__(self):
        self._resolution_size = ss.get_resolution_index()

    def get_font(self, font_size: FontSize, font_style: FontStyle):
        scale = self._resolution_size + ss.game_units_to_px(4)
        size = font_size.value + scale
        return pygame.font.Font(font_style.value, size)
