import pygame
from animation import Animation

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class Player:
    def __init__(
            self,
            right_jump: pygame.Surface,
            left_jump: pygame.Surface,
            static: pygame.Surface,
            right_animation: Animation,
            left_animation: Animation
    ):
        self.right_jump = right_jump
        self.left_jump = left_jump
        self.static = static
        self.right_animation = right_animation
        self.left_animation = left_animation

        self.sprite = self.static
        self.player_rect = self.sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    @staticmethod
    def scale(player_sprite: pygame.surface.Surface) -> pygame.surface.Surface:
        original_height = player_sprite.get_height()
        original_width = player_sprite.get_width()
        target_height = 80
        player_scale = target_height / original_height
        target_width = player_scale * original_width
        return pygame.transform.smoothscale(player_sprite, (target_width, target_height))

    @classmethod
    def load(cls) -> "Player":
        right_jump = Player.load_player_sprite("right_1")
        left_jump = Player.load_player_sprite("left_1")
        static = Player.load_player_sprite("static")

        right_animation = Animation(duration=10, frames=[
            Player.load_player_sprite("right_2"),
            Player.load_player_sprite("right_3"),
            Player.load_player_sprite("right_4")
        ])

        left_animation = Animation(duration=10, frames=[
            Player.load_player_sprite("left_2"),
            Player.load_player_sprite("left_3"),
            Player.load_player_sprite("left_4")
        ])

        return Player(right_jump, left_jump, static, right_animation, left_animation)

    @staticmethod
    def load_player_sprite(sprite_name: str) -> pygame.Surface:
        sprite = pygame.image.load(f"sprites/player/{sprite_name}.png")
        sprite = Player.scale(sprite)
        return sprite

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.sprite, self.player_rect)

