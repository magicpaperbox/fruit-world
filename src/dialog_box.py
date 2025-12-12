import pygame
from typing import List

from npcs import Npc
import scale_screen as ss

# MVVM
# M - Model (domain)
# VM - ViewModel
# V - View
class DialogBox:
    def __init__(self, *, rect, cps: int = 45, padding: int = 16):
        self.rect = rect
        self.cps = cps
        self.padding = padding

        self.queue: List[str] = []
        self.current: str = ""
        self.visible = False

        self._typed_len = 0
        self._time_acc = 0.0
        self._finished = False

        # # continue
        self._blink_timer = 0.0
        self._blink_on = True

        self._away_time = 0.0
        self._away_timeout_s = 2.0
        self._farewell_shown = False
        self._active_npc: Npc | None = None

    def show(self, text: str, npc: Npc | None = None):
        self.queue.clear()
        self.current = ""
        self.visible = True
        if npc is not None:
            self._active_npc = npc
        self.enqueue(text)

    def enqueue(self, text: str):
        self.queue.append(text)
        if not self.current:
            self._take_next()

    def hide(self):
        self.visible = False
        self.current = ""
        self.queue.clear()
        self._active_npc = None
        self._away_time = 0.0
        self.farewell_shown = False

    def handle_event(self, is_pick_pressed, is_exit_pressed, away, now_ms, dt_ms):
        dt = dt_ms / 1000.0

        if is_pick_pressed:
            self._away_time = 0.0
            self._farewell_shown = False
            if self.queue:
                self._take_next()
            else:
                self.hide()
            return
        if is_exit_pressed:
            self.hide()
        if away:
            if not self._farewell_shown and self._active_npc is not None:
                farewell_msg = self._active_npc.end_interaction(now_ms)
                if farewell_msg:
                    self.show(farewell_msg)
                self._farewell_shown = True
                self._away_time = 0.0

            self._away_time += dt
            if self._away_time >= self._away_timeout_s:
                self.hide()
        else:
            self._away_time = 0.0
            self._farewell_shown = False

    def update(self, dt_ms: int):
        if not self.visible or not self.current:
            return

        dt = dt_ms / 1000.0

        if not self._finished:
            self._time_acc += dt
            target_len = int(self._time_acc * self.cps)
            if target_len > self._typed_len:
                self._typed_len = min(len(self.current), target_len)
                if self._typed_len == len(self.current):
                    self._finished = True
        # blink
        self._blink_timer += dt
        if self._blink_timer >= 0.5:
            self._blink_timer = 0.0
            self._blink_on = not self._blink_on

# getters
    def should_draw(self) -> bool:
        return self.visible and bool(self.current)

    def get_text(self) -> str:
        return self.current

    def get_typed_len(self) -> int:
        return self._typed_len

    def is_finished(self) -> bool:
        return self._finished

    def is_blink_on(self) -> bool:
        return self._blink_on

# private
    def _take_next(self):
        self.current = self.queue.pop(0)
        self._typed_len = 0
        self._time_acc = 0.0
        self._finished = False


class DialogBoxView:
    def __init__(
        self,
        *,
        font: pygame.font.Font,
        text_color=(245, 245, 235),
        bg_color=(80, 100, 75),
        border_light=(140, 165, 135),
        border_dark = (65, 85, 60),
        radius: int = 12,
        border_w: int = 2,

    ):
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_light = border_light
        self.border_dark = border_dark
        self.radius = radius
        self.border_w = border_w

    def draw(self, screen: pygame.Surface, vm):
        if not vm.should_draw():
            return

        rect = vm.rect
        padding = vm.padding

#         # tło (białe) + ramka
        pygame.draw.rect(screen, self.bg_color, rect, border_radius=self.radius)
        pygame.draw.rect(screen, self.border_light, rect, width=self.border_w, border_radius=self.radius)
        shadow_rect = rect.inflate(2, 2).move(1, 1)
        pygame.draw.rect(screen, self.border_dark, shadow_rect, width=self.border_w, border_radius=self.radius)

#         # tekst
        inner_w = rect.width - 2 * padding
        inner_h = rect.height - 2 * padding
        x = rect.x + padding
        y = rect.y + padding

        typed = vm.get_text()[: vm.get_typed_len()]
        lines = self._wrap(typed, inner_w)
        line_h = self.font.get_linesize()
        max_lines = inner_h // line_h
        lines = lines[:max_lines]  # obetnij jakby było za dużo


        for i, ln in enumerate(lines):
            surf = self.font.render(ln, True, self.text_color)
            screen.blit(surf, (x, y + i * line_h))

        # wskaźnik “dalej”
        if vm.is_finished() and vm.is_blink_on():
            tri_x = rect.right - padding - 12
            tri_y = rect.bottom - padding - 8
            pygame.draw.polygon(
                screen,
                self.border_light,
                [(tri_x, tri_y), (tri_x + 12, tri_y), (tri_x + 6, tri_y + 8)],
            )

    def _wrap(self, text: str, max_w: int) -> List[str]:
        words = text.split(" ")
        lines: List[str] = []
        cur = ""
        for w in words:
            test = w if not cur else cur + " " + w
            if self.font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                while self.font.size(w)[0] > max_w:
                    cut = len(w)
                    while cut > 1 and self.font.size(w[:cut])[0] > max_w:
                        cut -= 1
                    lines.append(w[:cut])
                    w = w[cut:]
                cur = w
        if cur:
            lines.append(cur)
        return lines


def make_dialog_rect(screen_w: int, screen_h: int, box_height: int, margin: int) -> pygame.Rect:
    offset_x = (ss.SCREEN_WIDTH - screen_w) // 2
    width = screen_w - 2 * margin
    return pygame.Rect(
        offset_x + margin,
        screen_h - box_height - margin,
        width,
        box_height,
    )