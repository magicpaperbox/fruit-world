import pygame

from gameplay.player.player_health import Health
from render. sprite_factory import SPRITE_FACTORY

from screen import scale_screen as ss


class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item_id: str, amount: int = 1):
        # self.items.get("strawberry", 0) → nie istnieje → 0; 0 + 1 = 1
        self._items[item_id] = self._items.get(item_id, 0) + amount

    def remove(self, item_id: str, amount: int = 1):
        if item_id in self._items:
            new_amount = self._items[item_id] - amount
            if new_amount <= 0:
                del self._items[item_id]
            else:
                self._items[item_id] = new_amount

    def count(self, item_id: str) -> int:
        return self._items.get(item_id, 0)  # 0 <- to co dostaniemy jeśli klucz nie istnieje

    def all_items(self):
        return self._items.items()


class InventoryUI:
    def __init__(
        self,
        font: pygame.font.Font,
        item_icons: dict[str, pygame.Surface],
        panel: pygame.Rect,
        padding: float = ss.game_units_to_px(3),
        line_space: float = ss.game_units_to_px(5),
    ):
        self.font = font
        self.item_icons = item_icons
        self._panel = panel
        self._padding = padding
        self._line_space = line_space
        self._margin_x = ss.game_units_to_px(10)
        self._margin_y = ss.game_units_to_px(20)
        self._start_x = self._panel.left + self._margin_x
        self._start_y = self._panel.top + self._margin_y
        self._box_width = ss.game_units_to_px(75)
        self._box_height = ss.game_units_to_px(75)
        self._gap = ss.game_units_to_px(5)
        self.dark = (65, 85, 60)
        self.light = (140, 165, 135)
        self.slot_columns = 3
        self.slot_rows = 6
        self._slots = []

        for i in range(self.slot_rows):
            y = self._start_y + i * (self._box_height + self._gap)
            for j in range(self.slot_columns):
                x = self._start_x + j * (self._box_width + self._gap)
                slot = pygame.Rect(x, y, self._box_width, self._box_height)
                self._slots.append(slot)

    def draw(self, screen: pygame.Surface, inventory: Inventory, health: Health):
        self._draw_health(screen, health.health_points)
        items_list = list(inventory.all_items())
        for slot_index, slot in enumerate(self._slots):
            self._draw_slot(screen, slot)
            if slot_index < len(items_list):
                item_id, count = items_list[slot_index]
                self._draw_picked_item(screen, slot, item_id, count)

    def _draw_slot(self, screen, slot):
        pygame.draw.rect(screen, self.dark, slot, width=5, border_radius=10)
        pygame.draw.rect(screen, self.light, slot, width=3, border_radius=10)
        pygame.draw.rect(screen, self.dark, slot, width=1, border_radius=10)

    def _draw_picked_item(self, screen, slot, item_id, count):
        icon = self.item_icons.get(item_id)
        if icon:
            icon_rect = icon.get_rect(center=slot.center)
            screen.blit(icon, icon_rect)
            text = self.font.render(str(count), True, (255, 255, 255))
            text_rect = text.get_rect(bottomright=(slot.right - 4 * self._padding, slot.bottom - 2 * self._line_space))
            screen.blit(text, text_rect)

    def _draw_health(self, screen: pygame.Surface, count):
        icon_height = ss.relative_y_to_game_units_px(0.05)
        heart_icon = SPRITE_FACTORY.load("sprites/items/heart.png", icon_height)
        heart_rect = heart_icon.get_rect(bottomright=self._panel.bottomright)
        screen.blit(heart_icon, (heart_rect[0] - 6.5 * icon_height, heart_rect[1] - icon_height * 0.5))
        text = self.font.render(str(count), True, (255, 255, 255))
        screen.blit(text, (heart_rect[0] - 6 * icon_height, heart_rect[1] - icon_height * 0.25))