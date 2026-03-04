from enum import Enum

from render.sprite_factory import SPRITE_FACTORY
from screen.game_units import GameUnit


class Item(Enum):
    STRAWBERRY = ("strawberry", "sprites/items/strawberry.png")
    BLUEBERRY = ("blueberry", "sprites/items/blueberry.png")

    def __init__(self, item_id: str, sprite_path: str):
        self.item_id = item_id
        self.sprite_path = sprite_path
        self._icon_height = GameUnit(32).pixels

    def _load_single_icon(self):
        return SPRITE_FACTORY.load(self.sprite_path, self._icon_height)

    @classmethod
    def load_all_icons(cls):
        item_icons = {}
        for item in Item:
            item_icons[item.item_id] = item._load_single_icon()
        return item_icons
