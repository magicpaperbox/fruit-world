from typing import Self

import pygame

from gameplay.player.inventory import Inventory
from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from gameplay.player.player_mobility import PlayerMobility
from gameplay.player.player_money import Money
from gameplay.player.player_view import PlayerView
from render.debuggable import Debuggable
from render.drawable import Drawable
from render.sprite_object import SpriteObject
from screen.game_inputs import GameInputs


class Player(Drawable, Debuggable):
    def __init__(self, view: PlayerView, inventory: Inventory, mobility: PlayerMobility):
        self._view = view
        self._mobility = mobility
        self.money = Money()
        self.health = Health()
        self.mana = Mana()
        self.inventory = inventory

    def process_inputs(self, dt: int, inputs: GameInputs, obstacles: list[SpriteObject]):
        if inputs.is_right_pressed:
            self._mobility.move_right(obstacles, dt)
        elif inputs.is_left_pressed:
            self._mobility.move_left(obstacles, dt)

        if inputs.space_pressed_this_frame:
            self._mobility.jump()

        self._mobility.move_vertically(obstacles, dt)

    def set_x_position(self, x: int) -> None:
        self._mobility.set_x_position(x)

    @property
    def player_rect(self):
        return self._mobility.visual_rect

    @classmethod
    def load(cls, gravity: float) -> Self:
        return Player(PlayerView.load(), Inventory(), PlayerMobility(gravity))

    def update_sprite(self, inputs: GameInputs, dt_ms: int) -> None:
        self._view.update_sprite(
            self._mobility.is_on_ground,
            inputs.is_right_pressed,
            inputs.is_left_pressed,
            self._mobility.coordinates,
            dt_ms,
        )

    def draw(self, screen: pygame.surface.Surface):
        self._view.draw(screen)

    def draw_debug(self, screen: pygame.surface.Surface):
        self._mobility.draw_debug(screen)
