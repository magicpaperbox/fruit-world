import pygame

type _CacheKey = tuple[str, int]


class SpriteFactory:
    def __init__(self):
        self._sprite_cache: dict[_CacheKey, pygame.Surface] = {}

    def load(self, sprite_path: str, target_height_px: int) -> pygame.Surface:
        key: _CacheKey = (sprite_path, target_height_px)
        if key not in self._sprite_cache:
            self._sprite_cache[key] = SpriteFactory._load_uncached(sprite_path, target_height_px)
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

    @staticmethod
    def _scale_by_width(sprite: pygame.surface.Surface, target_width: int):
        original_height = sprite.get_height()
        original_width = sprite.get_width()
        object_scale = target_width / original_width
        target_height = int(object_scale * original_height)
        return pygame.transform.smoothscale(sprite, (target_width, target_height))

    def load_by_width(self, sprite_path: str, target_width_px: int) -> pygame.Surface:
        key: _CacheKey = (sprite_path, target_width_px)
        if key not in self._sprite_cache:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = SpriteFactory._scale_by_width(sprite, target_width_px)
            self._sprite_cache[key] = sprite
        return self._sprite_cache[key]


SPRITE_FACTORY = SpriteFactory()
