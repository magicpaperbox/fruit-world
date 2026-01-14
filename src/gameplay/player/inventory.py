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
            new_amount = self._items[item_id] - amount
            if  new_amount <= 0:
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
        self.padding = padding
        self.line_space = line_space

    def _create_slots(self, screen, inventory):
        margin_x = ss.game_units_to_px(10)
        margin_y = ss.game_units_to_px(20)
        start_x = self._panel.left + margin_x
        start_y = self._panel.top + margin_y
        box_width = ss.game_units_to_px(75)
        box_height = ss.game_units_to_px(75)
        gap = ss.game_units_to_px(5)
        dark = (65, 85, 60)
        light = (140, 165, 135)
        items_list = list(inventory.all_items())
        slot_index = 0
        for i in range(6):
            y = start_y + i * (box_height + gap)
            for j in range(3):
                x = start_x + j * (box_width + gap)
                slot = pygame.Rect(x, y, box_width, box_height)
                pygame.draw.rect(screen, dark, slot, width=5, border_radius=10)
                pygame.draw.rect(screen, light, slot, width=3, border_radius=10)
                pygame.draw.rect(screen, dark, slot, width=1, border_radius=10)

                if slot_index < len(items_list):
                    item_id, count = items_list[slot_index]
                    icon = self.item_icons.get(item_id)
                    if icon:
                        icon_rect = icon.get_rect(center=slot.center)
                        screen.blit(icon, icon_rect)
                        text = self.font.render(str(count), True, (255, 255, 255))
                        text_rect = text.get_rect(bottomright=(slot.right - 4*self.padding, slot.bottom - 2*self.line_space))
                        screen.blit(text, text_rect)
                slot_index += 1

    def draw(self, screen: pygame.Surface, inventory: Inventory):
        self._create_slots(screen, inventory)
 