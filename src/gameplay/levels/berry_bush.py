import random

import pygame

from gameplay.levels.inventory_item_template import InventoryItemTemplate
from render.sprite_object import SpriteObject
from screen.game_units import GameUnit


class BerryBush(SpriteObject):
    def __init__(
        self,
        rect: pygame.Rect,
        berry_template: InventoryItemTemplate,
        berries_initial_count: int,
        bush: pygame.Surface,
    ):
        super().__init__(sprite=bush, rect=rect)
        self._berry_template = berry_template
        self._berries = self._spawn_berries(berries_initial_count)

    @property
    def berry_item_id(self) -> str:
        return self._berry_template.id

    def try_pick_berries(self, player_rect: pygame.Rect) -> int:
        for berry in self._berries[:]:  # kopia, bo modyfikujemy listę
            if player_rect.colliderect(berry.rect):
                pygame.mixer.Sound("sounds/item_pick_up.wav").play().set_volume(0.7)
                self._berries.remove(berry)
                return 1
        return 0

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        for berry in self._berries:
            berry.draw(screen)

    def _spawn_berries(self, berries_amount: int):
        berry_height_px = GameUnit(40).pixels
        sprite = self._berry_template.load_sprite(berry_height_px)
        jitter_px = GameUnit(36).pixels
        rnd = random.Random()
        berries: list[SpriteObject] = []
        if berries_amount <= 0:
            return

        b = self.rect

        horizontal_margin_pct = 0.15
        vertical_margin_px = berry_height_px // 2

        x_min = b.x + int(horizontal_margin_pct * b.width)
        x_max = b.x + int((1 - horizontal_margin_pct) * b.width)
        y_min = b.y + vertical_margin_px * 2
        y_max = b.y + b.height - vertical_margin_px

        slot_w = (x_max - x_min) / max(1, berries_amount)  # nie dzieli przez 0
        jx_max = int(min(jitter_px, int(slot_w * 0.1)))

        for i in range(berries_amount):
            base_x = x_min + (i + 0.5) * slot_w
            x = base_x + (rnd.randint(-jx_max, jx_max) if jx_max > 0 else 0)
            y = rnd.randint(int(y_min), int(y_max))
            berry = SpriteObject.create(sprite, center=(x, y))
            berries.append(berry)

        return berries
