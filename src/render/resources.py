import pygame

from gameplay.player.player_health import Health
from gameplay.player.player_mana import Mana
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss


class DrawResources:
    def __init__(self, font: pygame.font.Font):
        self.icon_height = ss.relative_y_to_game_units_px(0.05)
        self.font = font
        self.y = ss.relative_y_to_game_units_px(0.03)
        self.offset_x = 1.06
        self.offset_y = 1.4
        self.heart_icon = SPRITE_FACTORY.load("sprites/items/heart.png", self.icon_height)
        self.mana_icon = SPRITE_FACTORY.load("sprites/items/mana_potion.png", self.icon_height)

    def _draw_resource(self, screen: pygame.Surface, count, icon, x):
        x = ss.relative_x_to_game_units_px(x)
        screen.blit(icon, (x, self.y))
        text = self.font.render(str(count), True, (255, 255, 255))
        screen.blit(text, (x * self.offset_x, self.y * self.offset_y))

    def draw(self, screen: pygame.Surface, health: Health, mana: Mana):
        self._draw_resource(screen, health.health_points, self.heart_icon, 0.8)
        self._draw_resource(screen, mana.mana_points, self.mana_icon, 0.9)
