from enum import Enum

import pygame

from screen import scale_screen as ss
from screen.game_units import GameUnit


class FontSize(Enum):
    SMALL = 10
    MEDIUM = 15
    LARGE = 20
    XLARGE = 30


class FontStyle(Enum):
    CAPS_CONDENSED = "fonts/AmaticSC.ttf"
    CAPS_CONDENSED_BOLD = "fonts/AmaticSC-Bold.ttf"
    ORNATE = "fonts/Delius.ttf"
    SIMPLE = "fonts/Fredoka.ttf"
    HANDWRITTING = "fonts/LaBelleAurore.ttf"
    RUSTIC = "fonts/PrincessSofia.ttf"


type _CacheKey = tuple[FontStyle, FontSize]


class FontsFactory:
    def __init__(self):
        self._resolution_size = ss.get_resolution_index()
        self._font_cache: dict[_CacheKey, pygame.font.Font] = {}

    def get_font(self, font_size: FontSize, font_style: FontStyle) -> pygame.font.Font:
        cache_key = (font_style, font_size)
        if font_style in self._font_cache:
            return self._font_cache[cache_key]

        scale = self._resolution_size + GameUnit(4).pixels
        size = font_size.value + scale
        font = pygame.font.Font(font_style.value, size)

        self._font_cache[cache_key] = font
        return font
