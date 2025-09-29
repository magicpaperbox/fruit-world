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
        self._right_jump = right_jump
        self._left_jump = left_jump
        self._static = static
        self._right_animation = right_animation
        self._left_animation = left_animation


        self._sprite = self._static
        self.player_rect = self._sprite.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

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

    def update_sprite(self, on_ground: bool, is_right_pressed: bool, is_left_pressed: bool) -> None:
        if is_right_pressed:
            facing_dir = "right"
        elif is_left_pressed:
            facing_dir = "left"
        else:
            facing_dir = "front"
        if not on_ground:
            if facing_dir == "right":
                self._sprite = self._right_jump
            elif facing_dir == "left":
                self._sprite = self._left_jump
            else:
                self._sprite = self._static
        else:
            if facing_dir == "right":
                self._right_animation.advance()
                self._sprite = self._right_animation.sprite
            elif facing_dir == "left":
                self._left_animation.advance()
                self._sprite = self._left_animation.sprite
            else:
                self._sprite = self._static


    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self._sprite, self.player_rect)
