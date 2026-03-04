from gameplay.levels.inventory_item_template import InventoryItemTemplate


class Inventory:
    def __init__(self):
        self._items: dict[InventoryItemTemplate, int] = {}

    def add(self, item_template: InventoryItemTemplate, amount: int = 1):
        self._items[item_template] = self._items.get(item_template, 0) + amount

    def remove(self, item_template: InventoryItemTemplate, amount: int = 1):
        if item_template in self._items:
            new_amount = self._items[item_template] - amount
            if new_amount <= 0:
                del self._items[item_template]
            else:
                self._items[item_template] = new_amount

    def count(self, item_template: InventoryItemTemplate) -> int:
        return self._items.get(item_template, 0)

    def all_items(self):
        return self._items.items()
