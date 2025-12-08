import enum

import pygame
from animation import Animation
import scale_screen

SCREEN_WIDTH, SCREEN_HEIGHT = scale_screen.GAME_WIDTH, scale_screen.GAME_HEIGHT


class Status(str, enum.Enum):
    STANDBY = "standby"
    HELLO = "hello"


class Npc:
    _sprite_cache: dict[tuple[str, int], pygame.Surface] = {}

    def __init__(
        self,
        x: int,
        y: int,
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

        # tymczasowa podmiana animacji
        self._override_surface: pygame.Surface | None = None
        self._override_until_ms: int = 0
        # jednorazowa animacja
        self._override_anim: Animation | None = None
        self._override_anim_until_ms: int = 0
        self._status = Status.STANDBY

    def interaction(self, now_ms: int) -> str | None:
        if self._status == Status.STANDBY:
            self.show_frame("hello", ms=800, now_ms=now_ms)
            message = "Hello my friend!"
            self._status = Status.HELLO
            return message

    def end_interaction(self, now_ms: int) -> str | None:
        message = None
        if self._status == Status.HELLO:
            self.play_once(self._bye_bye_animation, ms=800, now_ms=now_ms)
            message = "Bye bye!"
        self._status = Status.STANDBY
        return message

    def show_frame(self, kind: str, ms: int, now_ms: int):
        mapping = {
            "hello": self._hello,
            "happy": self._interaction,
            "thinking": self._quest_update,
        }
        self._override_surface = mapping[kind]
        self._override_until_ms = now_ms + ms
        self._override_anim = None

    def play_once(self, anim: Animation, ms: int, now_ms: int):
        # Pokaż jednorazową animację przez ms milisekund
        self._override_anim = anim.copy() if hasattr(anim, "copy") else anim
        self._override_anim_until_ms = now_ms + ms
        self._override_surface = None

    @staticmethod
    def scale(npc_sprite: pygame.surface.Surface) -> pygame.Surface:
        original_height = npc_sprite.get_height()
        original_width = npc_sprite.get_width()
        target_height = scale_screen.GAME_HEIGHT * 0.1
        npc_scale = target_height / original_height
        target_width = int(round(npc_scale * original_width))
        return pygame.transform.smoothscale(npc_sprite, (target_width, target_height))

    @classmethod
    def load_mouse(cls, x: int, y: int) -> "Npc":
        thinking = Npc.load_npc_sprite("npc_mouse_thinking")
        happy = Npc.load_npc_sprite("npc_mouse_happy")
        hello = Npc.load_npc_sprite("npc_mouse_hi")

        mouse = Npc.load_npc_sprite("npc_mouse")
        blink = Npc.load_npc_sprite("npc_mouse_standby")

        frames = [mouse] * 25 + [blink]
        standby_animation = Animation(duration=10, frames=frames)
        bye_animation = Animation(duration=10, frames=[cls.load_npc_sprite("npc_mouse_bye"), mouse])

        return Npc(x, y, standby_animation, hello, happy, thinking, bye_animation)

    @staticmethod
    def load_npc_sprite(sprite_name: str) -> pygame.Surface:
        key = (sprite_name, 70)
        if key not in Npc._sprite_cache:
            surf = pygame.image.load(f"sprites/npc/{sprite_name}.png").convert_alpha()
            Npc._sprite_cache[key] = Npc.scale(surf)
        return Npc._sprite_cache[key]

    def center(self, new_frame):
        if new_frame.get_size() != self._sprite.get_size():
            cx, by = self.npc_rect.centerx, self.npc_rect.bottom
            self.npc_rect = new_frame.get_rect(centerx=cx, bottom=by)
        self._sprite = new_frame

    def update_sprite(self, now_ms: int):
        # jednorazowa animacja
        if self._override_anim and now_ms < self._override_anim_until_ms:
            self._override_anim.advance()
            new_frame = self._override_anim.surface()
            self.center(new_frame)
            return
        else:
            self._override_anim = None

        # tymczasowa statyczna klatka
        if self._override_surface and now_ms < self._override_until_ms:
            new_frame = self._override_surface
            self.center(new_frame)
            return
        else:
            self._override_surface = None

        self._static.advance()
        new_frame = self._static.surface()
        self.center(new_frame)

    def draw(self, screen: pygame.Surface):
        screen.blit(self._sprite, self.npc_rect)
