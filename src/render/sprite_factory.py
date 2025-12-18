import pygame

type _CacheKey = tuple[str, int]

class SpriteFactory:

    def __init__(self):
        self._sprite_cache: dict[_CacheKey, pygame.Surface] = {}

    def load(self, sprite_path: str, target_height: int) -> pygame.Surface:
        key: _CacheKey = (sprite_path, target_height)
        if key not in self._sprite_cache:
            self._sprite_cache[key] = SpriteFactory._load_uncached(sprite_path, target_height)
        return self._sprite_cache[key]

    @staticmethod
    def _load_uncached(sprite_path: str, target_height: int) -> pygame.Surface:
        sprite = pygame.image.load(sprite_path).convert_alpha()
        sprite = SpriteFactory._scale(sprite, target_height)
        return sprite

    @staticmethod
    def _scale(sprite: pygame.surface.Surface, target_height: int) -> pygame.Surface:
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_height / original_height
        target_width = int(object_scale * original_width)
        return pygame.transform.smoothscale(sprite, (target_width, target_height))
