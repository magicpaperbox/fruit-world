import pygame

from screen import scale_screen as ss


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item_id: str, amount: int = 1):
        # self.items.get("strawberry", 0) → nie istnieje → 0; 0 + 1 = 1
        self._items[item_id] = self._items.get(item_id, 0) + amount

    def remove(self, item_id: str, amount: int = 1):
        if item_id in self._items:
            self._items[item_id] = max(0, self._items[item_id] - amount)  # max(a, b) zwraca większą z dwóch wartości

    def count(self, item_id: str) -> int:
        return self._items.get(item_id, 0)  # 0 <- to co dostaniemy jeśli klucz nie istnieje

    def all_items(self):
        return self._items.items()


class InventoryUI:
    def __init__(
        self,
        font: pygame.font.Font,
        item_icons: dict[str, pygame.Surface],
        padding: float = ss.game_units_to_px(3),
        line_space: float = ss.game_units_to_px(5),
    ):
        self.font = font
        self.item_icons = item_icons
        self.padding = padding
        self.line_space = line_space

    def draw(self, screen: pygame.Surface, inventory: Inventory, x: int, y: int):
        ox = x
        oy = y
        for item_id, count in inventory.all_items():
            icon = self.item_icons.get(item_id)
            row_height = 0
            if icon is not None:
                icon_rect = icon.get_rect(topleft=(ox, oy))
                screen.blit(icon, icon_rect)
                text_x = icon_rect.right + self.padding // 2
                row_height = icon_rect.height
            else:
                # jak nie ma ikonki – sam tekst
                text_x = ox

            text = self.font.render(str(count), True, (255, 255, 255))

            if row_height > 0:
                text_y = oy + (row_height - text.get_height()) // 2
                row_height = max(row_height, text.get_height())
            else:
                text_y = oy
                row_height = text.get_height()

            screen.blit(text, (text_x, text_y))

            # 3) następna linia
            oy += row_height + self.line_space
