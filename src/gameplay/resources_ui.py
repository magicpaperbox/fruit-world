import pygame

from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from gameplay.player.player_money import Money
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss
from screen.game_units import GameUnit


class ResourcesUI:
    def __init__(self, font: pygame.font.Font):
        self._font = font

        self._y = ss.relative_y_to_game_units_px(0.03)

        icon_height = ss.relative_y_to_game_units_px(0.05)
        self._heart_icon = SPRITE_FACTORY.load("sprites/items/heart.png", icon_height)
        self._mana_icon = SPRITE_FACTORY.load("sprites/items/mana_potion.png", icon_height)
        self._money_icon = SPRITE_FACTORY.load("sprites/items/nut_money.png", icon_height)

    def draw(self, screen: pygame.Surface, money: Money, health: Health, mana: Mana):
        self._draw_resource(screen, money.money_points, self._money_icon, 0.7)
        self._draw_resource(screen, health.health_points, self._heart_icon, 0.8)
        self._draw_resource(screen, mana.mana_points, self._mana_icon, 0.9)

    def _draw_resource(self, screen: pygame.Surface, count: int, icon: pygame.Surface, x_pct: float):
        x = ss.relative_x_to_game_units_px(x_pct)
        screen.blit(icon, (x, self._y))
        text = self._font.render(str(count), True, (255, 255, 255))

        text_y = self._y + (icon.get_height() // 2) - (text.get_height() // 2)
        text_x = x + icon.get_width() + GameUnit(15).pixels

        screen.blit(text, (text_x, text_y))
