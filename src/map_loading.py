import pygame
from scale_screen import GAME_WIDTH, GAME_HEIGHT, relative_coords_to_game_units_px


class Map:
    def __init__(self, sprite: pygame.surface.Surface):
        self.sprite = sprite
        self.rect = sprite.get_rect(center=relative_coords_to_game_units_px(0.5, 0.5))

    @staticmethod
    def scale(direction_image: pygame.surface.Surface) -> pygame.surface.Surface:
        return pygame.transform.smoothscale(direction_image, (GAME_WIDTH, GAME_HEIGHT))

    @classmethod
    def load(cls, sprite_name: str) -> "Map":
        sprite = pygame.image.load(f"sprites/map/{sprite_name}.png")
        sprite = cls.scale(sprite)
        return Map(sprite)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)
