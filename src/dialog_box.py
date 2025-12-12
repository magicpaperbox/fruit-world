import pygame
from typing import List

from npcs import Npc
import scale_screen

# class TalkToNPC:
#     def __init__(self):
#         self.queue: List[str] = []
#         self.current: str = ""
#         self._blink_timer = 0.0
#         self._blink_on = True
#         self.visible = False
#         self._away_time = 0.0
#         self._away_timeout_s = 2.0
#         self._farewell_shown = False
#         self._active_npc = None
#
#     def show(self, text: str, npc: Npc | None = None):
#         self.queue.clear()
#         self.current = ""
#         self.visible = True
#         if npc is not None:
#             self._active_npc = npc
#         return self.enqueue(text)
#
#     def enqueue(self, text: str):
#         self.queue.append(text)
#         if not self.current:
#             self._take_next()
#         return self
#
#     def _hide(self):
#         self.visible = False
#         self.current = ""
#         self.queue.clear()
#         self._away_counter = 0
#         self._active_npc = None
#
#     def _take_next(self):
#         self.current = self.queue.pop(0)
#         self._typed_len = 0
#         self._time_acc = 0.0
#         self._finished = False
#
#     def handle_event(self, is_pick_pressed, is_exit_pressed, away, now_ms, dt_ms):
#         dt = dt_ms / 1000.0
#         if is_pick_pressed:
#             self._away_time = 0.0
#             self._farewell_shown = False
#             if self.queue:
#                 self._take_next()
#             else:
#                 self._hide()
#             return
#         if is_exit_pressed:
#             self._hide()
#         if away:
#             if not self._farewell_shown and self._active_npc is not None:
#                 farewell_msg = self._active_npc.end_interaction(now_ms)
#                 if farewell_msg:
#                     self.show(farewell_msg)
#                 self._farewell_shown = True
#                 self._away_time = 0.0
#             self._away_time += dt
#             if self._away_time >= self._away_timeout_s:
#                 self._hide()
#         else:
#             self._away_time = 0.0
#             self._farewell_shown = False

# MVVM
# M - Model (domain)
# VM - ViewModel
# V - View

# class DialogBox:
#     def show_text(self, text: str):
#         pass
#
#
# dialog.show_text("Hello", self._show_how_are_you)
#
# dialog.show_text("How are you?", ["yes", "no"], self._on_answer)
#
# def _on_answer(answer: str):
#     if answer == "yes":
#         dialog.show_text("ok. good")
#         dialog.hide()
#     else:
#         dialog.show_text("uuu, I can help")
#         player.health += 10
#         dialog.show_text("are you bettter?",  ["yes", "no"], self._on_other_answer)


class DialogBox:
    def __init__(
        self,
        screen_w: int,
        screen_h: int,
        font: pygame.font.Font,
        text_color=(245, 245, 235),
        bg_color=(80, 100, 75),
        border_color=(130, 155, 125),
        box_height=scale_screen.DIALOG_HEIGHT,
        margin=12,
        padding=16,
        cps=45,  # chars per second (efekt pisania)
    ):
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.cps = cps

        width = screen_w - 2 * margin
        self.rect = pygame.Rect(margin, screen_h - box_height - margin, width, box_height)

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
        self._active_npc = None

    def show(self, text: str, npc: Npc | None = None):
        self.queue.clear()
        self.current = ""
        self.visible = True
        if npc is not None:
            self._active_npc = npc
        return self.enqueue(text)

    def enqueue(self, text: str):
        self.queue.append(text)
        if not self.current:
            self._take_next()
        return self

    def _hide(self):
        self.visible = False
        self.current = ""
        self.queue.clear()
        self._away_counter = 0
        self._active_npc = None

    def handle_event(self, is_pick_pressed, is_exit_pressed, away, now_ms, dt_ms):
        dt = dt_ms / 1000.0
        if is_pick_pressed:
            self._away_time = 0.0
            self._farewell_shown = False
            if self.queue:
                self._take_next()
            else:
                self._hide()
            return
        if is_exit_pressed:
            self._hide()
        if away:
            if not self._farewell_shown and self._active_npc is not None:
                farewell_msg = self._active_npc.end_interaction(now_ms)
                if farewell_msg:
                    self.show(farewell_msg)
                self._farewell_shown = True
                self._away_time = 0.0
            self._away_time += dt
            if self._away_time >= self._away_timeout_s:
                self._hide()
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

    def draw(self, screen: pygame.Surface):
        if not self.visible or not self.current:
            return

        # tło (białe) + ramka
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=12)

        # tekst (zawijanie do szerokości)
        inner_w = self.rect.width - 2 * self.padding
        inner_h = self.rect.height - 2 * self.padding
        x = self.rect.x + self.padding
        y = self.rect.y + self.padding

        lines = self._wrap(self.current[: self._typed_len], inner_w)
        line_h = self.font.get_linesize()
        max_lines = inner_h // line_h
        lines = lines[:max_lines]  # obetnij jakby było za dużo

        for i, ln in enumerate(lines):
            surf = self.font.render(ln, True, self.text_color)
            screen.blit(surf, (x, y + i * line_h))

        # wskaźnik “dalej”
        if self._finished and self._blink_on:
            tri_x = self.rect.right - self.padding - 12
            tri_y = self.rect.bottom - self.padding - 8
            pygame.draw.polygon(
                screen,
                self.border_color,
                [(tri_x, tri_y), (tri_x + 12, tri_y), (tri_x + 6, tri_y + 8)],
            )

    def _take_next(self):
        self.current = self.queue.pop(0)
        self._typed_len = 0
        self._time_acc = 0.0
        self._finished = False

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
                # jeśli pojedyncze słowo dłuższe niż max_w – tniemy “na twardo”
                while self.font.size(w)[0] > max_w:
                    # szukaj najdłuższego pasującego prefiksu
                    cut = len(w)
                    while cut > 1 and self.font.size(w[:cut])[0] > max_w:
                        cut -= 1
                    lines.append(w[:cut])
                    w = w[cut:]
                cur = w
        if cur:
            lines.append(cur)
        return lines
