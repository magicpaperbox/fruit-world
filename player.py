import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class Player:
    def __init__(self, sprite: pygame.surface.Surface):
        self.sprite = sprite
        self.player_rect = sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    @staticmethod
    def scale(player_sprite: pygame.surface.Surface) -> pygame.surface.Surface:
        original_height = player_sprite.get_height()
        original_width = player_sprite.get_width()
        target_height = 80
        player_scale = target_height / original_height
        target_width = player_scale * original_width
        return pygame.transform.smoothscale(player_sprite, (target_width, target_height))

    @classmethod
    def load(cls, sprite_name: str) -> "Player":
        sprite = pygame.image.load(f"sprites/player/{sprite_name}.png")
        sprite = cls.scale(sprite)
        return Player(sprite)

    def draw(self, player: pygame.surface.Surface):
        player.blit(self.sprite, self.player_rect)
