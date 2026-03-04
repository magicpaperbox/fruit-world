from enum import Enum

import pygame

from render.sprite_factory import SPRITE_FACTORY
from screen.game_units import GameUnit


class InventoryItemTemplate(Enum):
    STRAWBERRY = "strawberry"
    BLUEBERRY = "blueberry"

    def __init__(self, item_id: str):
        self.id = item_id
        self.sprite_path = f"sprites/items/{item_id}.png"

    def load_sprite(self, icon_height: int) -> pygame.Surface:
        return SPRITE_FACTORY.load(self.sprite_path, icon_height)

    @classmethod
    def load_all_icons_for_inventory(cls):
        icon_height = GameUnit(32).pixels
        item_icons = {}
        for item in InventoryItemTemplate:
            item_icons[item.id] = item.load_sprite(icon_height)
        return item_icons
