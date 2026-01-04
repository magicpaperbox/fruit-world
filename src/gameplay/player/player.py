import pygame
from render.animation import Animation
from screen import scale_screen as ss
from render.sprite_factory import SPRITE_FACTORY


class Player:
    def __init__(
        self,
        right_jump: pygame.Surface,
        left_jump: pygame.Surface,
        static: pygame.Surface,
        right_animation: Animation,
        left_animation: Animation,
    ):
        self._right_jump = right_jump
        self._left_jump = left_jump
        self._static = static
        self._right_animation = right_animation
        self._left_animation = left_animation

        self._sprite = self._static
        self.player_rect = self._sprite.get_rect(center=(ss.relative_coords_to_game_units_px(0.5, 0.5)))

    @classmethod
    def load(cls) -> "Player":
        height = ss.relative_y_to_game_units_px(0.1)

        def load_player_sprite(sprite_name: str) -> pygame.Surface:
            return SPRITE_FACTORY.load(f"sprites/player/{sprite_name}.png", height)

        right_jump = load_player_sprite("right_1")
        left_jump = load_player_sprite("left_1")
        static = load_player_sprite("static")

        right_animation = Animation(
            duration=10,
            frames=[
                load_player_sprite("right_2"),
                load_player_sprite("right_3"),
                load_player_sprite("right_4"),
            ],
        )

        left_animation = Animation(
            duration=10,
            frames=[
                load_player_sprite("left_2"),
                load_player_sprite("left_3"),
                load_player_sprite("left_4"),
            ],
        )

        return Player(right_jump, left_jump, static, right_animation, left_animation)

    def update_sprite(
        self,
        on_ground: bool,
        is_right_pressed: bool,
        is_left_pressed: bool,
        coordinates: tuple[int, int],
    ) -> None:
        self.player_rect.x = coordinates[0]
        self.player_rect.y = coordinates[1]
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
