from typing import Self

import pygame

from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from gameplay.player.player_view import PlayerView
from render.drawable import Drawable


class Player(Drawable):
    def __init__(self, view: PlayerView):
        self._view = view
        self.health = Health()
        self.mana = Mana()

    @property
    def player_rect(self):
        return self._view.player_rect

    @classmethod
    def load(cls) -> Self:
        return cls(PlayerView.load())

    def update_sprite(
        self, on_ground: bool, is_right_pressed: bool, is_left_pressed: bool, coordinates: tuple[int, int], dt_ms: int
    ) -> None:
        self._view.update_sprite(on_ground, is_right_pressed, is_left_pressed, coordinates, dt_ms)

    def draw(self, screen: pygame.surface.Surface):
        self._view.draw(screen)
