import pygame


class Strawberry:
    def __init__(self, sprite: pygame.surface.Surface, x: int, y: int):
        self.sprite = sprite
        self.rect = sprite.get_rect(center=(x, y))

    @staticmethod
    def scale(sprite: pygame.surface.Surface, target_height: int) -> pygame.surface.Surface:
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_height / original_height
        target_width = object_scale * original_width
        return pygame.transform.smoothscale(sprite, (target_width, target_height))

    @classmethod
    def load(cls, sprite_name: str, target_height: int, x: int, y: int) -> "Strawberry":
        sprite = pygame.image.load(f"sprites/items/{sprite_name}.png")
        sprite = cls.scale(sprite, target_height)
        return Strawberry(sprite, x, y)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)
        # screen.fill((0, 255, 0))

