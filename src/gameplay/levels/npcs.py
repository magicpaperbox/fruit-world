import enum

import pygame

from gameplay.levels.dialog import DialogStep
from render.animation import Animation
from screen import scale_screen as ss
from gameplay.levels.quest import Quest
from render.sprite_factory import SPRITE_FACTORY


class Status(str, enum.Enum):
    STANDBY = "standby"
    HELLO = "hello"


class Npc:
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
        default_dialog: list[DialogStep],
    ):
        self.npc_id = npc_id
        self._current_quest: Quest | None = None
        self._static = static
        self._hello = hello
        self._interaction = interaction
        self._quest_update = quest_update
        self._bye_bye_animation = bye_bye_animation
        self._dialog_index = 0
        self._dialog: list[DialogStep] = []
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

    def set_dialog(self, dialog_steps: list[DialogStep]):  # step = {"text": "Hello", "frame": "hello", "ms": 800}
        self._dialog = dialog_steps
        self._dialog_index = 0
        self._is_in_dialog = False

    def interaction(self, now_ms: int) -> DialogStep | None:
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
        frame = step.frame

        if frame:
            self.show_frame(frame, ms=1000, now_ms=now_ms)
        has_next = self._dialog_index < len(self._dialog) - 1
        if has_next:
            self._dialog_index += 1
        else:
            self._dialog_index = 0
            self._is_in_dialog = False
            self._status = Status.HELLO
        return step

    def end_interaction(self, now_ms: int) -> DialogStep | None:
        message = None
        if self._status == Status.HELLO:
            self.play_once(self._bye_bye_animation, ms=500, now_ms=now_ms)
            message = DialogStep("Bye bye!", "hello", speaker="Mouse")
            pygame.mixer.Sound("sounds/npc_hmhm.wav").play()
            self._dialog_index = 0
            self._is_in_dialog = False
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
    def load_npc_sprite(sprite_name: str) -> pygame.Surface:
         height = ss.relative_y_to_game_units_px(0.1)
         return SPRITE_FACTORY.load(f"sprites/npc/{sprite_name}.png", height)

    @classmethod
    def load_mouse(cls, x: int, y: int) -> "Npc":
        thinking = Npc.load_npc_sprite("mouse/thinking")
        happy = Npc.load_npc_sprite("mouse/happy")
        hello = Npc.load_npc_sprite("mouse/welcome")

        mouse = Npc.load_npc_sprite("mouse/static")
        blink = Npc.load_npc_sprite("mouse/blink")

        frames = [mouse] * 30 + [blink]
        standby_animation = Animation(duration=100, frames=frames)
        bye_animation = Animation(duration=200, frames=[cls.load_npc_sprite("mouse/bye"), mouse])

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
                DialogStep("Hello my friend!", frame="hello", speaker="Mouse"),
            ],
        )

        return npc


    def center(self, new_frame):
        if new_frame.get_size() != self._sprite.get_size():
            cx, by = self.npc_rect.centerx, self.npc_rect.bottom
            self.npc_rect = new_frame.get_rect(centerx=cx, bottom=by)
        self._sprite = new_frame

    def update_sprite(self, now_ms: int, dt_ms: int):
        # jednorazowa animacja
        if self._override_anim and now_ms < self._override_anim_until_ms:
            self._override_anim.advance(dt_ms)
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

        self._static.advance(dt_ms)
        new_frame = self._static.surface()
        self.center(new_frame)

    def draw(self, screen: pygame.Surface):
        screen.blit(self._sprite, self.npc_rect)
