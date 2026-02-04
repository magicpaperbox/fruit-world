from enum import Enum

import pygame

from screen import scale_screen


class FontType(Enum):
    DIALOG = 8
    INVENTORY = 9
    RESOURCES = 14
    OTHER = 10


class FontFamily(Enum):
    BASIC = "sprites/fonts/AmaticSC.ttf"
    BASIC_BOLD = "sprites/fonts/AmaticSC-Bold.ttf"
    PRETTY = "sprites/fonts/Delius.ttf"
    DIALOG = "sprites/fonts/Fredoka.ttf"
    HANDWRITTING = "sprites/fonts/LaBelleAurore.ttf"
    TITLES = "sprites/fonts/PrincessSofia.ttf"


class FontsFactory:
    def __init__(self):
        self.resolution_size = scale_screen.get_font_size()

    def get_font(self, font_type: FontType, font_family: FontFamily):
        enlarge = self.resolution_size - 8
        size = font_type.value + enlarge
        return pygame.font.Font(font_family.value, size)
