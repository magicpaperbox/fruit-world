import enum

import pygame
from render.animation import Animation
from screen import scale_screen as ss
from gameplay.levels.quest import Quest


class Status(str, enum.Enum):
    STANDBY = "standby"
    HELLO = "hello"


class Npc:
    _sprite_cache: dict[tuple[str, int], pygame.Surface] = {}

    def __init__(
        self,
        npc_id: str,
        x: int,
        y: int,
        static: Animation,
        hello: pygame.Surface,
        interaction: pygame.Surface,
        quest_update: pygame.Surface,
        bye_bye_animation: Animation,
        default_dialog: list[dict],
    ):
        self.npc_id = npc_id
        self._current_quest: Quest | None = None
        self._static = static
        self._hello = hello
        self._interaction = interaction
        self._quest_update = quest_update
        self._bye_bye_animation = bye_bye_animation
        self._dialog_index = 0
        self._dialog = []
        self._sprite = self._static.surface()
        self._default_dialog = default_dialog
        self.npc_rect = self._sprite.get_rect(midbottom=(x, y))

        # tymczasowa podmiana animacji
        self._override_surface: pygame.Surface | None = None
        self._override_until_ms: int = 0
        # jednorazowa animacja
        self._override_anim: Animation | None = None
        self._override_anim_until_ms: int = 0
        self._status = Status.STANDBY
        self._is_in_dialog = False
        self.set_dialog(default_dialog)

    def set_quest(self, quest: Quest):
        self._current_quest = quest

    def clear_quest(self):
        self._current_quest = None

    def set_dialog(self, dialog_steps: list[dict]):  # step = {"text": "Hello", "frame": "hello", "ms": 800}
        self._dialog = dialog_steps
        self._dialog_index = 0
        self._is_in_dialog = False

    def interaction(self, now_ms: int) -> str | None:
        if not self._is_in_dialog:
            if self._current_quest is not None:
                dialog = self._current_quest.get_current_dialog(self.npc_id)
                if dialog:
                    self.set_dialog(dialog)
                else:
                    self.set_dialog(self._default_dialog)
            else:
                self.set_dialog(self._default_dialog)
            self._is_in_dialog = True

        if not self._dialog:
            return None
        step = self._dialog[self._dialog_index]
        frame = step.get("frame")
        ms = step.get("ms", 800)
        text = step.get("text")

        if frame:
            self.show_frame(frame, ms=ms, now_ms=now_ms)
            mode = step.get("mode", "next")
            if mode == "next":
                if self._dialog_index < len(self._dialog) - 1:
                    self._dialog_index += 1
                elif mode == "stay":
                    pass
                elif mode == "end":
                    self._dialog_index = 0
                    self._is_in_dialog = False
            self._status = Status.HELLO
            return text

    def end_interaction(self, now_ms: int) -> str | None:
        message = None
        if self._status == Status.HELLO:
            self.play_once(self._bye_bye_animation, ms=800, now_ms=now_ms)
            message = "Bye bye!"
            pygame.mixer.Sound("sounds/npc_hmhm.wav").play()
            self._dialog_index = 0
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
        target_height = ss.relative_y_to_game_units_px(0.1)
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

        npc = Npc(
            "mouse",
            x,
            y,
            standby_animation,
            hello,
            happy,
            thinking,
            bye_animation,
            [
                {"text": "Hello my friend!", "frame": "hello", "ms": 800, "mode": "next", "quest": 0, "react": False},
            ],
        )

        return npc

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
