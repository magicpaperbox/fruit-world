import pygame
from typing import Self

class SpriteObject:
    def __init__(self, sprite: pygame.Surface, x: int, y: int):
        self.sprite = sprite
        self.rect = sprite.get_rect(center=(x, y))

    @classmethod
    def load(cls, sprite_path: str, target_height: int, x: int, y: int) -> Self:
        sprite = pygame.image.load(sprite_path)
        sprite = cls.scale(sprite, target_height)
        return cls(sprite, x, y)

    @staticmethod
    def scale(sprite: pygame.surface.Surface, target_height: int) -> pygame.Surface:
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_height / original_height
        target_width = int(object_scale * original_width)
        return pygame.transform.smoothscale(sprite, (target_width, target_height))


    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)

    # @classmethod
    # def load(cls, sprite_name: str) -> Self:
    #     sprite_path = f"sprites/map/{sprite_name}.png"
    #     x, y = relative_coords_to_game_units_px(0.5, 0.5)
    #     return super().load(sprite_path, target_height=GAME_HEIGHT, x=x, y=y)
