import pygame

from screen import scale_screen as ss
from screen.game_units import GameUnit


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item_id: str, amount: int = 1):
        self._items[item_id] = self._items.get(item_id, 0) + amount

    def remove(self, item_id: str, amount: int = 1):
        if item_id in self._items:
            new_amount = self._items[item_id] - amount
            if new_amount <= 0:
                del self._items[item_id]
            else:
                self._items[item_id] = new_amount

    def count(self, item_id: str) -> int:
        return self._items.get(item_id, 0)  # 0 <- if no key

    def all_items(self):
        return self._items.items()


class InventoryUI:
    def __init__(
        self,
        font: pygame.font.Font,
        item_icons: dict[str, pygame.Surface],
        panel: pygame.Rect,
    ):
        self._font = font
        self._item_icons = item_icons
        self._panel = panel
        self._padding = GameUnit(8).pixels
        self._line_space = GameUnit(5).pixels
        self._margin_x = GameUnit(10).pixels
        self._margin_y = GameUnit(20).pixels
        self._border = ss.game_units_to_px_min(3)
        self._border_radius = GameUnit(15).pixels
        self._start_x = self._panel.left + self._margin_x
        self._start_y = self._panel.top + self._margin_y
        self._box_width = GameUnit(75).pixels
        self._box_height = GameUnit(75).pixels
        self._gap = GameUnit(5).pixels
        self._dark = (65, 85, 60)
        self._light = (140, 165, 135)
        self._slot_columns = 2
        self._slot_rows = 13
        self._slots = []

        for i in range(self._slot_rows):
            y = self._start_y + i * (self._box_height + self._gap)
            for j in range(self._slot_columns):
                x = self._start_x + j * (self._box_width + self._gap)
                slot = pygame.Rect(x, y, self._box_width, self._box_height)
                self._slots.append(slot)

    def draw(self, screen: pygame.Surface, inventory: Inventory):
        items_list = list(inventory.all_items())
        for slot_index, slot in enumerate(self._slots):
            self._draw_slot(screen, slot)
            if slot_index < len(items_list):
                item_id, count = items_list[slot_index]
                self._draw_picked_item(screen, slot, item_id, count)

    def _draw_slot(self, screen: pygame.Surface, slot: pygame.Rect):
        shadow_rect = slot.inflate(self._border, self._border).move(1, 1)
        pygame.draw.rect(screen, self._dark, shadow_rect, width=ss.game_units_to_px_min(7), border_radius=self._border_radius)
        pygame.draw.rect(screen, self._light, slot, width=ss.game_units_to_px_min(3), border_radius=self._border_radius)

    def _draw_picked_item(self, screen: pygame.Surface, slot: pygame.Rect, item_id: str, count: int):
        icon = self._item_icons.get(item_id)
        if icon:
            icon_rect = icon.get_rect(center=slot.center)
            screen.blit(icon, icon_rect)
            text = self._font.render(str(count), True, (255, 255, 255))
            text_rect = text.get_rect(bottomright=(slot.right - self._padding, slot.bottom))
            screen.blit(text, text_rect)
