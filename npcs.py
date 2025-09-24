import pygame
from animation import Animation

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class Npc:
    def __init__(
            self,
            x:int,
            y:int,
            static: Animation,
            hello: pygame.Surface,
            interaction: pygame.Surface,
            quest_update: pygame.Surface,
            bye_bye_animation: Animation,
    ):

        self._static = static
        self._hello = hello
        self._interaction = interaction
        self._quest_update = quest_update
        self._bye_bye_animation = bye_bye_animation

        self._sprite = self._static.surface()
        self.npc_rect = self._sprite.get_rect(midbottom=(x, y))

    @staticmethod
    def scale(npc_sprite: pygame.surface.Surface) -> pygame.Surface:
        original_height = npc_sprite.get_height()
        original_width = npc_sprite.get_width()
        target_height = 70
        npc_scale = target_height / original_height
        target_width = int(round(npc_scale * original_width))
        return pygame.transform.smoothscale(npc_sprite, (target_width, target_height))

    @classmethod
    def load_mouse(cls, x: int, y: int) -> "Npc":
        thinking = Npc.load_npc_sprite("npc_mouse_thinking")
        happy = Npc.load_npc_sprite("npc_mouse_happy")
        hello = Npc.load_npc_sprite("npc_mouse_hi")

        standby_animation = Animation(duration=10, frames=[
            Npc.load_npc_sprite("npc_mouse"),
            Npc.load_npc_sprite("npc_mouse_standby")
        ])

        bye_animation = Animation(duration=10, frames=[
            Npc.load_npc_sprite("npc_mouse_bye"),
            Npc.load_npc_sprite("npc_mouse")
        ])

        return Npc(x, y, standby_animation, hello, happy, thinking, bye_animation)

    @staticmethod
    def load_npc_sprite(sprite_name: str) -> pygame.Surface:
        sprite = pygame.image.load(f"sprites/npc/{sprite_name}.png")
        return Npc.scale(sprite)


    def update_sprite(self):
        self._static.advance()
        new_frame = self._static.surface()
        if new_frame.get_size() != self._sprite.get_size():
            cx, by = self.npc_rect.centerx, self.npc_rect.bottom
            self.npc_rect = new_frame.get_rect(centerx=cx, bottom=by)
        self._sprite = new_frame

    def draw(self, screen: pygame.Surface):
        screen.blit(self._sprite, self.npc_rect)