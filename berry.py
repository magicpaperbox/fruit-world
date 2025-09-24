import pygame


class Berry:
    def __init__(self, sprite: pygame.Surface, x: int, y: int):
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
    def load(cls, sprite_name: str, target_height: int, x: int, y: int) -> "Berry":
        sprite = pygame.image.load(f"sprites/items/{sprite_name}.png")
        sprite = cls.scale(sprite, target_height)
        return Berry(sprite, x, y)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.rect)
        # screen.fill((0, 255, 0))

def pick_berry(berries: list, player_rect: pygame.Rect, is_pick_pressed: bool) -> int:
    if not is_pick_pressed:
        return 0
    picked = 0
    for berry in berries[:]:  # kopia, bo modyfikujemy listę
        if berry.rect.colliderect(player_rect):
            berries.remove(berry)
            picked += 1
    return picked
