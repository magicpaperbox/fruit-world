import pygame


class SpriteFactory:

    def load(self, sprite_path: str, target_height: int) -> pygame.Surface:
        sprite = pygame.image.load(sprite_path)
        sprite = SpriteFactory._scale(sprite, target_height)
        return sprite

    @staticmethod
    def _scale(sprite: pygame.surface.Surface, target_height: int) -> pygame.Surface:
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_height / original_height
        target_width = int(object_scale * original_width)
        return pygame.transform.smoothscale(sprite, (target_width, target_height))
