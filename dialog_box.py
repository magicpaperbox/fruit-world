import pygame
from typing import List, Optional

class DialogBox:
    def __init__(
        self,
        screen_w: int,
        screen_h: int,
        font: pygame.font.Font,
        text_color=(0, 0, 0),
        bg_color=(255, 255, 255),
        border_color=(30, 30, 30),
        box_height=160,
        margin=12,
        padding=16,
        cps=45,  # chars per second (efekt pisania)
    ):
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.cps = cps

        width = screen_w - 2 * margin
        self.rect = pygame.Rect(margin, screen_h - box_height - margin, width, box_height)

