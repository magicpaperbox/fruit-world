import pygame
import random
from screen import scale_screen as ss
from render.sprite_factory import SPRITE_FACTORY
from render.sprite_object import SpriteObject


class BerryBush(SpriteObject):
    def __init__(self, rect: pygame.Rect, berry_sprite_path: str, berries_initial_count: int, berry_item_id: str,
                 bush: pygame.Surface):
        super().__init__(sprite=bush, rect=rect)
        self._berry_sprite_path = berry_sprite_path
        self._berries = self._spawn_berries(berries_initial_count)
        self.berry_item_id = berry_item_id

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

    def _spawn_berries(self, berries_count: int):
        berry_height_px = ss.game_units_to_px(42)
        sprite = SPRITE_FACTORY.load(self._berry_sprite_path, berry_height_px)
        jitter_px = ss.game_units_to_px(36)
        rnd = random.Random()
        berries: list[SpriteObject] = []
        if berries_count <= 0:
            return

        b = self.rect

        horizontal_margin_pct = 0.15
        vertical_margin_px = berry_height_px // 2

        x_min = b.x + int(horizontal_margin_pct * b.width)
        x_max = b.x + int((1 - horizontal_margin_pct) * b.width)
        y_min = b.y + vertical_margin_px * 2
        y_max = b.y + b.height - vertical_margin_px

        slot_w = (x_max - x_min) / max(1, berries_count)  # nie dzieli przez 0
        jx_max = int(min(jitter_px, int(slot_w * 0.1)))

        for i in range(berries_count):
            base_x = x_min + (i + 0.5) * slot_w
            x = base_x + (rnd.randint(-jx_max, jx_max) if jx_max > 0 else 0)
            y = rnd.randint(int(y_min), int(y_max))
            berry = SpriteObject.create(sprite, center=(x, y))
            berries.append(berry)

        return berries
