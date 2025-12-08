import pygame


class StaticObject:
    def __init__(self, sprite: pygame.Surface, x: int, y: int):
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center=(x, y))

    @staticmethod
    def load_sprite(name: str) -> pygame.Surface:
        return pygame.image.load(f"sprites/objects/{name}.png")

    @staticmethod
    def scale(sprite: pygame.Surface, target_height: int) -> pygame.Surface:
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_height / original_height
        target_width = object_scale * original_width
        return pygame.transform.smoothscale(sprite, (target_width, target_height))

    @classmethod
    def load(cls, name: str, target_height: int, x: int, y: int) -> "StaticObject":
        sprite = cls.load_sprite(name)
        sprite = cls.scale(sprite, target_height)
        return cls(sprite, x, y)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.sprite, self.rect)
