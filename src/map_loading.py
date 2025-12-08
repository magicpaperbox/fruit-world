import pygame
import scale_screen

SCREEN_WIDTH, SCREEN_HEIGHT = scale_screen.GAME_WIDTH, scale_screen.GAME_HEIGHT


class Map:
    def __init__(self, sprite: pygame.surface.Surface):
        self.sprite = sprite
        self.rect = sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    @staticmethod
    def scale(direction_image: pygame.surface.Surface) -> pygame.surface.Surface:
        return pygame.transform.smoothscale(direction_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    @classmethod
    def load(cls, sprite_name: str) -> "Map":
        sprite = pygame.image.load(f"sprites/map/{sprite_name}.png")
        sprite = cls.scale(sprite)
        return Map(sprite)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)
